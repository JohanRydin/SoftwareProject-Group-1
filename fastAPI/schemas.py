from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    userID: int
    username: str

    class Config:
        orm_mode = True  


class GenreBase(BaseModel):
    Name: str

class GenreCreate(GenreBase):
    pass  #TODO

class Genre(GenreBase):
    genreID: int

    class Config:
        orm_mode = True  


class GamePrefBase(BaseModel):
    userID: int
    gameID: int

class GamePrefCreate(GamePrefBase):
    pass  #TODO

class GamePref(GamePrefBase):
    class Config:
        orm_mode = True

class WishlistBase(BaseModel):
    userID: int
    gameID:int

class Wishlist(WishlistBase):
    class Config:
        orm_mode = True

class WishlistCreate(WishlistBase):
    pass #TODO

class WishlistUpdate(WishlistBase):
    pass #TODO

class WishlistRemove(WishlistBase):
    pass #TODO 

class WishlistDelete(WishlistBase):
    pass #TODO

class GenrePrefBase(BaseModel):
    userID: int
    genreID: int

class GenrePref(GenrePrefBase):
    class Config: 
        orm_mode = True 

class GenrePrefAdd(GenrePref):
    pass #TODO 

class GenrePrefUpdate(GenrePref):
    pass #TODO

class GenrePrefRemove(GenrePref):
    pass #TODO

class GenrePrefDelete(GenrePref):
    pass #TODO


class RecommendationRequest(BaseModel):
    username: str