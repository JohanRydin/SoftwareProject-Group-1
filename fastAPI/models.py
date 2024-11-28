from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "User"
    
    userID = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
