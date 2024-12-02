from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from models import User, Wishlist, GamePref, GenrePref
from schemas import UserCreate, UserResponse
import os
import requests
import httpx

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@db:3306/storage")

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

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

@app.get("/recommendation")
async def post_recommendation(): #(username: str, db: Session = Depends(get_db)):
    
    #db_user = db.query(User).filter(User.username == username).first()

    #if not db_user:
    #    raise HTTPException(status_code=404, detail="User not found")

    api_url = "http://aiserver:5000/recommendations"

    items = {"user": {"id": 5, "game_ids": [3, 5], "genres": ["Action", "Strategy", "Adventure"]}, "rows": [{"similar_to_games": [1, 7, 3]}, {"similar_to_games": "all"}, 
    {"similar_to_genre": "Sports"}, {"best_reviewed": "Adventure"}, {"best_sales": "Action"}]}

    async with httpx.AsyncClient() as client:
        # Make a POST request to the external API with JSON data
        response = await client.post(api_url, json=items)
        print(response)
    # Return the response from the external API
        return {"status_code": response.status_code, "response": response.json()}
    return response


