import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlmodel import Session, SQLModel, create_engine, Field, Relationship
from typing import Optional, List
#from models import User, GenrePref
import os

'''
This is a hack solution to get our database structure into the test-database
'''
class User(SQLModel, table=True):
    __tablename__ = "user"

    userID: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    
    # Relationships
    genre_prefs: List["GenrePref"] = Relationship(back_populates="user")
    wishlist: List["Wishlist"] = Relationship(back_populates="user")
    game_prefs: List["GamePref"] = Relationship(back_populates="user")


class Genre(SQLModel, table=True):
    __tablename__ = "genre"
    
    genreID: int = Field(primary_key=True, index=True)
    genrename: str = Field(unique=True, nullable=False)

    # Relationships
    genre_prefs: List["GenrePref"] = Relationship(back_populates="genre")


class Game(SQLModel, table=True):
    __tablename__ = "game"
    
    gameID: int = Field(primary_key=True, index=True)
    gamename: str = Field(unique=True, nullable=False, max_length=50)
    shortdescription: str = Field(nullable=False, max_length=300)
    genres: str = Field(nullable=False, max_length=300) 

    # Relationships
    wishlist: List["Wishlist"] = Relationship(back_populates="game")
    game_prefs: List["GamePref"] = Relationship(back_populates="game")


class GamePref(SQLModel, table=True):
    __tablename__ = "gamepref"
    
    userID: int = Field(foreign_key="user.userID", primary_key=True)
    gameID: int = Field(foreign_key="game.gameID", primary_key=True)

    # Relationships
    user: Optional[User] = Relationship(back_populates="game_prefs")
    game: Optional[Game] = Relationship(back_populates="game_prefs")


class Wishlist(SQLModel, table=True):
    __tablename__ = "wishlist"
    
    userID: int = Field(foreign_key="user.userID", primary_key=True)
    gameID: int = Field(foreign_key="game.gameID", primary_key=True)

    # Relationships
    user: Optional[User] = Relationship(back_populates="wishlist")
    game: Optional[Game] = Relationship(back_populates="wishlist")


class GenrePref(SQLModel, table=True):
    __tablename__ = "genrepref"
    
    userID: int = Field(foreign_key="user.userID", primary_key=True)
    genreID: int = Field(foreign_key="genre.genreID", primary_key=True)

    # Relationships
    user: Optional[User] = Relationship(back_populates="genre_prefs")
    genre: Optional[Genre] = Relationship(back_populates="genre_prefs")

TEST_DB_PATH = "testing.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

# Clean up the test database before running tests (we dont want it to stay)
def clean_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

# Reusable (fake)database engine for tests
@pytest.fixture(scope="function")
def test_engine():
    clean_test_db()
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine) 
    yield engine
    clean_test_db() 

# Reusable session fixture
@pytest.fixture(scope="function")
def test_session(test_engine):
    with Session(test_engine) as session:
        yield session

# Override the FastAPI `get_db` dependency
@pytest.fixture(scope="function")
def override_get_db(test_session):
    def _override_get_db():
        return test_session
    app.dependency_overrides[get_db] = _override_get_db
    yield
    app.dependency_overrides.clear()

# Use the reusable fixtures in tests
client = TestClient(app)


def populate_database(test_session): 
    users = [
    User(userID=1, username="first_user"),
    User(userID=2, username="another_user"),
    User(userID=3, username="third_user"),
    ]
    test_session.add_all(users)
    test_session.commit()

    
# -------- TESTS ---------- #

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Root url"}
    
# WARNING: override_get_db is greyed out but is necessary!!!! 
def test_get_users(override_get_db, test_session):
    populate_database(test_session)
    # Test the API endpoint
    response = client.get("/users")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0] == {"userID": 1, "username": "first_user"}
    

# WARNING: override_get_db is greyed out but is necessary!!!! 
def test_get_user(override_get_db, test_session):
    
    populate_database(test_session)

    # Test the API endpoint
    response = client.get("/user/first_user")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert data == {"userID": 1, "username": "first_user"}
    
    