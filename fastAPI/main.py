from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import User, Wishlist, GamePref, GenrePref, Genre
from schemas import UserCreate, UserResponse, RecommendationBody
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

# ------------- API ENDPOINTS ------------ #

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


@app.get("/user/{username}/wishlist", response_model=List[int])
async def get_wishlist(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    return await fetch_dbUserWishlist(userId, db)


@app.get("/user/{username}/gamepref", response_model=List[int])
async def get_wishlist(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    return await fetch_dbUsergamePref(userId, db)


@app.get("/user/{username}/genrepref", response_model=List[int])
async def get_wishlist(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    return await fetch_dbUsergenrePref(userId, db)

@app.post("/recommendation")
async def post_recommendation(
    recommendationBody: RecommendationBody,
    db: Session = Depends(get_db)
):
    # Fetch user preferences from the database
    game_ids = await fetch_dbUsergamePref(recommendationBody.user.userID, db)
    print(f"Game IDs: {game_ids}")
    genre_ids = await fetch_dbUsergenrePref(recommendationBody.user.userID, db)
    print(f"Genre Names: {genre_ids}")
    genre_names = await fetch_dbgenreNameFetch(genre_ids, db)
    print(f"Genrenames: {genre_names}")

    # Convert the Pydantic model to a dictionary
    newbody = recommendationBody.dict()  # Convert the Pydantic model to a dictionary
    print(f"Newbody before changes: {newbody}")

    # Ensure 'user' key exists in newbody and assign values
    
    newbody["user"]["game_ids"] = game_ids  # Set the game_ids
    newbody["user"]["genres"] = genre_names  # Set the genres

    # Return the updated body
    # return {"status_code": 200, "response": newbody}
    # External API URL
    api_url = "http://aiserver:5000/recommendations"

    async with httpx.AsyncClient() as client:
        # Make a POST request to the external API with the updated body
        response = await client.post(api_url, json=newbody)
        
        # Print and return the response
        print(response)
        return {"status_code": response.status_code, "response": response.json()}
