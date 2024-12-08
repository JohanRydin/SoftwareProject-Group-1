from pydantic import BaseModel
from typing import Any, List, Optional


class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    userID: int
    username: str

    class Config:
        orm_mode = True  

class User(BaseModel):
    userID: int
    game_ids: Optional[List[int]] = []  # Optional, default to empty list
    genres: Optional[List[str]] = []   # Optional, default to empty list

    class Config:
        orm_mode = True

class WishlistBase(BaseModel):
    userID: int
    gameID:int

class Wishlist(WishlistBase):
    class Config:
        orm_mode = True

class WishlistItem(BaseModel): 
    gameID: int


class RecommendationBody(BaseModel):
    rows: List[Any]