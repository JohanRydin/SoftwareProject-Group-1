from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import SessionLocal, Base
from models import User, Wishlist, GamePref, GenrePref, Genre, Game
from schemas import UserCreate, UserResponse, WishlistItem, RecommendationBody, GamePrefItem, GenrePrefItem
import httpx
import asyncio
from rapidfuzz import process, fuzz 
'''
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@db:3306/storage")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
'''
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


@app.on_event("startup")
async def initialize_global_games():
    global globalGamenames
    retries = 20 
    delay = 1  

    for attempt in range(retries):
        try:
            with SessionLocal() as db:
                globalGamenames = await fetchAllGameNames(db)
            if globalGamenames is not None:
                break
        except Exception as e:
            if attempt < retries - 1:
                await asyncio.sleep(delay)
                print("waiting for database connection")
                delay += 2 
            else:
                raise RuntimeError("Failed to connect to the database during startup.") from e

@app.on_event("startup")
async def initialize_global_games():
    global globalGamenames
    with SessionLocal() as db:
        globalGamenames = await fetchAllGameNames(db)

async def fetchAllGameNames(db: Session):
    games = db.query(Game.gamename).all()
    return [game[0] for game in games]

        
async def fetch_dbUser(username: str, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

async def create_dbUser(username: str, db: Session=Depends(get_db)):
    db_user = db.query(User).filter(User.username == username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username taken")
    new_user = User(username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user) 
    return await fetch_dbUser(username, db) 
    
    
async def fetch_dbUserWishlist(userId: int, db: Session=Depends(get_db)): 
    db_wishlist = db.query(Wishlist.gameID).filter(Wishlist.userID == userId).all()
    game_ids = [gameID for gameID, in db_wishlist]
    return game_ids

async def fetch_dbUsergamePref(userId: int, db: Session=Depends(get_db)): 
    db_gamePref = db.query(GamePref.gameID).filter(GamePref.userID == userId).all()
    game_ids = [gameID for gameID, in db_gamePref]
    return game_ids

async def fetch_dbUsergenrePref(userId: int, db: Session = Depends(get_db)):
    db_genrePref = db.query(Genre.genreID).join(GenrePref, Genre.genreID == GenrePref.genreID).filter(GenrePref.userID == userId).all()
    genrenames = [genre[0] for genre in db_genrePref]
    return genrenames

async def fetch_dbgenreNameFetch(genreId: List[int], db: Session = Depends(get_db)):
    result = (
        db.query(Genre.genreID, Genre.genrename)
        .filter(Genre.genreID.in_(genreId))
        .order_by(Genre.genreID)  
        .all()
    )
    genrelist = [genre.genrename for genre in result]
    return genrelist



async def fetch_dbGame(ids: List[int], db: Session = Depends(get_db)):
    games = db.query(Game).filter(Game.gameID.in_(ids)).all()
    game_list = [
        {
            "id": game.gameID,
            "gamename": game.gamename,
            "description": game.shortdescription,
            "genres": game.Genres,
        }
        for game in games
    ]
    return game_list

async def fetch_dbGameName(ids: List[int], db: Session=Depends(get_db)):
    games = db.query(Game).filter(Game.gameID.in_(ids)).all()
    return games

async def fetch_searchedGameMatches(input: str, db:Session=Depends(get_db)): 
    lst = []
    games = db.query(Game.gameID).filter(Game.gamename.ilike(f'{input}%')).all()
    lst = [game[0] for game in games]
    lst = await fetch_dbGame(lst, db)
    return lst

async def fetch_searchedGenreMatches(input: str, db:Session=Depends(get_db)): 
    lst = []
    genre = db.query(Genre.genreID).filter(Genre.genrename.ilike(f'{input}%')).all()
    lst = [g[0] for g in genre]
    lst = await fetch_dbgenreNameFetch(lst, db)
    return lst


# ------------- User ENDPOINTS ------------ #

@app.get("/")
async def check_server_root(): 
    return {"message": "Root url"}
'''
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
'''
@app.get("/users/", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.get("/user/{username}", response_model=UserResponse)
async def get_user(username: str, db: Session = Depends(get_db)):
    return await fetch_dbUser(username, db)

@app.post("/user/{username}")
async def create_user(username: str, db: Session = Depends(get_db)):
    attempt = await create_dbUser(username, db)
    return attempt

# ----- Wishlist endpoints ----- # 

@app.get("/user/{username}/wishlist")
async def get_wishlist(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    gameIDs = await fetch_dbUserWishlist(userId, db)
    gameObjectList = await fetch_dbGame(gameIDs, db)
    return gameObjectList


@app.post("/user/{username}/wishlist")
async def post_to_wishlist(username: str, wishlist_item: WishlistItem, db: Session = Depends(get_db)):
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
        db.rollback()   
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

        return {"message": "Game removed from wishlist", "wishlist_entry": {"userID": userId, "gameID": item}}

    except Exception as e:
        db.rollback()   
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the game from the wishlist: {e}")
    
# WARNING: Deletes entire wishlist
@app.delete("/user/{username}/wishlist")
async def delete_entire_wishlist(username: str, db: Session = Depends(get_db)):
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
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the wishlist: {e}")



# ------ Genrepref endpoints ------ # 

@app.get("/user/{username}/genrepref", response_model=List[str])
async def get_genrepref(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    genreIDList = await fetch_dbUsergenrePref(userId, db)
    genreList = await fetch_dbgenreNameFetch(genreIDList, db)
    return genreList 


@app.post("/user/{username}/genrepref")
async def post_to_genrepref(username: str, genreItem: GenrePrefItem, db: Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID

    try:
        genre = db.query(Genre).filter(Genre.genrename == genreItem.genrename).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre name not found")

        genreID = genre.genreID

        existing_entry = db.query(GenrePref).filter(GenrePref.userID == userId, GenrePref.genreID == genreID).first()
        if existing_entry:
            raise HTTPException(status_code=400, detail="Genre is already in the genrePref")

        new_entry = GenrePref(userID=userId, genreID=genreID)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return {"message": "Genre added", "Entry": {"userID": userId, "genrename": genreItem.genrename}}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while adding to the genrePref: {e}")



@app.delete("/user/{username}/genrepref/{genrename}")
async def remove_specific_genrepref(username: str, genrename: str, db: Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID

    try:
        genre = db.query(Genre).filter(Genre.genrename == genrename).first()
        if not genre:
            raise HTTPException(status_code=404, detail="Genre name not found")

        genreID = genre.genreID

        existing_entry = db.query(GenrePref).filter(GenrePref.userID == userId, GenrePref.genreID == genreID).first()
        if not existing_entry:
            raise HTTPException(status_code=400, detail="Genre is not in the genrePref")

        db.delete(existing_entry)
        db.commit()

        return {"message": "Genre removed from GenrePref", "removed": {"userID": userId, "genrename": genrename}}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the genre from the genrePref: {e}")
    


@app.delete("/user/{username}/genrepref")
async def delete_entire_genrepref(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID  

    try:
        entries = db.query(GenrePref).filter(GenrePref.userID == userId).all()
        
        if not entries:
            raise HTTPException(status_code=404, detail="No genrePref entries found for this user")

        for entry in entries:
            db.delete(entry)

        db.commit()
        return {"message": "All genrePres removed from genrePref"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the genrePref: {e}")

# ----- GamePref endpoints ---------- # 

@app.get("/user/{username}/gamepref")
async def get_gamepref(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID
    gameIDList = await fetch_dbUsergamePref(userId, db)
    genreList = await fetch_dbGame(gameIDList, db)
    return genreList 


@app.post("/user/{username}/gamepref")
async def post_to_gamepref(username: str, gameItem: GamePrefItem, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID

    try:
        existing_entry = db.query(GamePref).filter(GamePref.userID == userId, GamePref.gameID == gameItem.gameID).first()
        if existing_entry:
            raise HTTPException(status_code=400, detail="Game is already in the gamePref")

        new_entry = GamePref(userID=userId, gameID=gameItem.gameID)
        db.add(new_entry)  
        db.commit() 
        db.refresh(new_entry)

        return {"message": "Game added", "Entry": {"userID": userId, "gameID":gameItem.gameID}}

    except Exception as e:
        db.rollback()   
        raise HTTPException(status_code=500, detail=f"An error occurred while adding to the gamePref: {e}")


@app.delete("/user/{username}/gamepref/{gameID}")
async def remove_specific_gamepref(username: str, gameID: int, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID  

    try:
        existing_entry = db.query(GamePref).filter(GamePref.userID == userId, GamePref.gameID == gameID).first()
        if not existing_entry:
            raise HTTPException(status_code=400, detail="Game is not in the gamepref")

        db.delete(existing_entry) 
        db.commit() 

        return {"message": "Game removed from gamePref", "gamePref": {"userID": userId, "gamePref": gameID}}

    except Exception as e:
        db.rollback()   
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the game from the gamePref: {e}")
    


@app.delete("/user/{username}/gamepref")
async def delete_entire_gamepref(username: str, db:Session = Depends(get_db)):
    userId = await fetch_dbUser(username, db)
    userId = userId.userID  

    try:
        entries = db.query(GamePref).filter(GamePref.userID == userId).all()
        
        if not entries:
            raise HTTPException(status_code=404, detail="No gamePref entries found for this user")

        for entry in entries:
            db.delete(entry)

        db.commit()
        return {"message": "All genrePres removed from GamePref"}

    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=f"An error occurred while removing the GamePref: {e}")



# ---- RECOMMENDATION endpoints ------ # 

async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client
        
@app.post("/user/{username}/recommendation")
async def get_recommended_games(
    username: str, 
    recommendationBody: RecommendationBody, 
    db: Session = Depends(get_db), 
    client: httpx.AsyncClient = Depends(get_http_client)
):
    userid = await fetch_dbUser(username, db)
    userid = userid.userID
    game_ids = await fetch_dbUsergamePref(userid, db)
    genre_ids = await fetch_dbUsergenrePref(userid, db)
    genre_names = await fetch_dbgenreNameFetch(genre_ids, db)

    newbody = recommendationBody.dict()
    newbody["user"] = {
        "userID": userid,
        "game_ids": game_ids,
        "genres": genre_names
    }

    api_url = "http://aiserver:5000/recommendations"
    response = await client.post(api_url, json=newbody)

    response_data = response.json()
    game_lists = response_data.get("games", [])
    game_names_lists = [await fetch_dbGame(game_list, db) for game_list in game_lists]

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

@app.get("/search/games")
async def get_searched_games(input:str, numbers: int, db:Session=Depends(get_db)): 

    all_titles = globalGamenames
    all_titles_lowercase = [title.lower() for title in globalGamenames]
    input = input.lower()

    matches = process.extract(input, all_titles_lowercase, scorer=fuzz.WRatio, limit=numbers)

    match_scores = {match[0]: match[1] for match in matches}

    names = [all_titles[all_titles_lowercase.index(match[0])] for match in matches]

    #games = db.query(Game).filter(
    #    func.lower(Game.gamename).in_([name.lower() for name in names])
    #).all()
    games = db.query(Game).filter(Game.gamename.in_(names)).all() 

    lst_with_scores = [
        {
            "id": game.gameID,
            "gamename": game.gamename, 
            "description": game.shortdescription,
            "genres": game.Genres,
            "score": match_scores.get(game.gamename.lower(), None)  
        }
        for game in games
    ]
    
    result = sorted(lst_with_scores, key=lambda x: x["score"], reverse=True)
    for game in result:
        del game["score"]

    return result


@app.get("/search/genres")
async def get_searched_genres(input:str, numbers: int, db:Session=Depends(get_db)): 
    lst = await fetch_searchedGenreMatches(input, db)
    lst = lst[:numbers]
    return  lst 
