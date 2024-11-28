from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str

class UserResponse(BaseModel):
    userID: int
    username: str

    class Config:
        orm_mode = True  # This allows SQLAlchemy models to be used with Pydantic
