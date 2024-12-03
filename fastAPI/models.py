from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base

class User(Base):
    __tablename__ = "User"
    
    userID = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)

class Genre(Base):
    __tablename__ = "Genre"
    genreID = Column(Integer, primary_key=True, index=True)
    genrename = Column(String(50), unique=True, nullable=False)

class Game(Base):
    __tablename__ = "Game"
    gameID = Column(Integer, primary_key=True, index=True)
    gamename = Column(String(50), unique=True, nullable=False)

class GamePref(Base):
    __tablename__ = "gamePref"
    userID = Column(Integer, ForeignKey("User.userID", ondelete="CASCADE"), primary_key=True)
    gameID = Column(Integer, primary_key=True)


class Wishlist(Base):
    __tablename__ = "wishlist"
    userID = Column(Integer, ForeignKey("User.userID", ondelete="CASCADE"), primary_key=True)
    gameID = Column(Integer, primary_key=True)


class GenrePref(Base):
    __tablename__ = "genrePref"
    userID = Column(Integer, ForeignKey("User.userID", ondelete="CASCADE"), primary_key=True)
    genreID = Column(Integer, ForeignKey("Genre.genreID", ondelete="CASCADE"), primary_key=True)



