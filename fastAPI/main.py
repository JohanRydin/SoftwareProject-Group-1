from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import User, Wishlist, GamePref, GenrePref, Genre, Game
from schemas import UserCreate, UserResponse, WishlistItem, RecommendationBody
import os
import requests
import httpx


DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@db:3306/storage")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()
origins = [
    "http://localhost:8080"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get the DB session
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def fetch_dbUser(username: str, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
    
async def fetch_dbUserWishlist(userId: int, db: Session=Depends(get_db)): 
    db_wishlist = db.query(Wishlist.gameID).filter(Wishlist.userID == userId).all()
    game_ids = [gameID for gameID, in db_wishlist]
    return game_ids

async def fetch_dbUsergamePref(userId: int, db: Session=Depends(get_db)): 
    db_gamePref = db.query(GamePref.gameID).filter(GamePref.userID == userId).all()
    game_ids = [gameID for gameID, in db_gamePref]
    return game_ids

async def fetch_dbUsergenrePref(userId: int, db: Session=Depends(get_db)): 
    db_genrePref = db.query(GenrePref.genreID).filter(GenrePref.userID == userId).all()
    genre_ids = [genreID for genreID, in db_genrePref]
    return genre_ids

async def fetch_dbgenreNameFetch(genreId: List[int], db: Session = Depends(get_db)):
    genrelist = []
    for id in genreId:
        # Flatten the result to get a list of genre names
        genres = [genre[0] for genre in db.query(Genre.genrename).filter(Genre.genreID == id).all()]
        genrelist.extend(genres)  # Add genres to the main list
    return genrelist

async def fetch_dbGame(ids: List[int], db: Session=Depends(get_db)):
    game_details_list = []
    
    for id in ids:
        # Query the database for all relevant details of the current game ID
        game = db.query(Game).filter(Game.gameID == id).first()

        # Ensure the game exists before proceeding
        if game:
            game_details = {
                "id": id,
                "gamename": game.gamename,
                "description": game.shortdescription,
                "genres": game.Genres
            }
            game_details_list.append(game_details)

    return game_details_list


# ------------- USER ENDPOINTS ------------ #

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/user/{username}", response_model=UserResponse)
async def get_user(username: str, db: Session = Depends(get_db)):
    return await fetch_dbUser(username, db)


# ----- Wishlist endpoints ----- # 

@app.get("/user/{username}/wishlist", response_model=List[int])
async def get_wishlist(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    return await fetch_dbUserWishlist(userId, db)


@app.post("/user/{username}/wishlist")
async def post_wishlist(username: str, wishlist_item: WishlistItem, db: Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID  

    try:
        existing_entry = db.query(Wishlist).filter(Wishlist.userID == userId, Wishlist.gameID == wishlist_item.gameID).first()
        if existing_entry:
            raise HTTPException(status_code=400, detail="Game is already in the wishlist")

        new_entry = Wishlist(userID=userId, gameID=wishlist_item.gameID)
        db.add(new_entry)  
        db.commit() 
        db.refresh(new_entry)

        return {"message": "Game added to wishlist", "wishlist_entry": {"userID": userId, "gameID": wishlist_item.gameID}}

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=500, detail=f"An error occurred while adding to the wishlist: {e}")


@app.delete("/user/{username}/wishlist/{item}")
async def remove_game_from_wishlist(username: str, item: int, db: Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID  

    try:
        existing_entry = db.query(Wishlist).filter(Wishlist.userID == userId, Wishlist.gameID == item).first()
        if not existing_entry:
            raise HTTPException(status_code=400, detail="Game is not in the wishlist")

        db.delete(existing_entry) 
        db.commit() 

        return {"message": "Game removed from wishlist", "wishlist_entry": {"userID": userId, "gameID": item.gameID}}

    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the game from the wishlist: {e}")
    
# WARNING: Deletes entire wishlist
@app.delete("/user/{username}/wishlist")
async def delete_wishlist(username: str, db: Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID  

    try:
        wishlist_entries = db.query(Wishlist).filter(Wishlist.userID == userId).all()
        
        if not wishlist_entries:
            raise HTTPException(status_code=404, detail="No wishlist entries found for this user")

        for entry in wishlist_entries:
            db.delete(entry)

        db.commit()
        return {"message": "All games removed from wishlist"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"An error occurred while adding to the wishlist: {e}")



# ------ GamePref endpoints ------ # 

@app.get("/user/{username}/gamepref", response_model=List[int])
async def get_gamepref(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    return await fetch_dbUsergamePref(userId, db)


@app.post("/user/{username}/genrepref", response_model=List[int])
async def post_gamepref(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    return await fetch_dbUsergenrePref(userId, db)



# ---- RECOMMENDATION endpoints ------ # 

@app.post("/user/{username}/recommendation")
async def post_recommendation(
    username: str, 
    recommendationBody: RecommendationBody, 
    db: Session = Depends(get_db)
):
    userid = await fetch_dbUser(username, db)
    userid = userid.userID
    game_ids = await fetch_dbUsergamePref(userid, db)
    genre_ids = await fetch_dbUsergenrePref(userid, db)
    genre_names = await fetch_dbgenreNameFetch(genre_ids, db)

    newbody = recommendationBody.dict() 
    
    # Ensure 'user' key exists in newbody and assign values
    newbody["user"] = {
        "userID": userid,        # Assign userID
        "game_ids": game_ids,    # Assign game IDs
        "genres": genre_names    # Assign genre names
    }
    
    # External API URL
    api_url = "http://aiserver:5000/recommendations"

    async with httpx.AsyncClient() as client:
        # Make a POST request to the external API with the updated body
        response = await client.post(api_url, json=newbody)
        
        # Convert game IDs to game names
        response_data = response.json()
        print(response_data)
        game_lists = response_data.get("games", [])
        print(game_lists)
        game_names_lists = [await fetch_dbGame(game_list, db) for game_list in game_lists]
        print(game_names_lists)
        
        # Return the response with game names
        return {"status_code": response.status_code, "response": {"games": game_names_lists}}

'''
POST:   http://localhost:8000/user/Erik/recommendation
{
    "rows": [
        {"similar_to_games": [1, 7, 3]},
        {"similar_to_games": "all"},
        {"similar_to_genre": "Sports"},
        {"best_reviewed": "Adventure"},
        {"best_sales": "Action"}
    ]
}
'''