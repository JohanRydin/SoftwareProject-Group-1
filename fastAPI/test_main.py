import pytest
from fastapi.testclient import TestClient
from pydantic import BaseModel
from main import app, get_db, get_http_client
from sqlmodel import Session, SQLModel, create_engine, Field, Relationship
from typing import Optional, List
import httpx 
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

# Thank god for chatGPT to generate fake data quickly
def populate_database(test_session): 
    # Create Users
    users = [
        User(userID=1, username="first_user"),
        User(userID=2, username="another_user"),
        User(userID=3, username="third_user"),
    ]
    test_session.add_all(users)
    test_session.commit()

    # Create Genres
    genres = [
        Genre(genreID=1, genrename="Action"),
        Genre(genreID=2, genrename="Adventure"),
        Genre(genreID=3, genrename="Puzzle"),
    ]
    test_session.add_all(genres)
    test_session.commit()

    # Create Games
    games = [
        Game(
            gameID=1,
            gamename="Action Game 1",
            shortdescription="An exciting action-packed adventure.",
            genres="Action, Adventure"
        ),
        Game(
            gameID=2,
            gamename="Puzzle Game 1",
            shortdescription="A challenging puzzle game for all ages.",
            genres="Puzzle"
        ),
        Game(
            gameID=3,
            gamename="Adventure Game 1",
            shortdescription="Explore and uncover secrets in this adventure game.",
            genres="Adventure"
        ),
    ]
    test_session.add_all(games)
    test_session.commit()

    # Create Genre Preferences
    genre_prefs = [
        GenrePref(userID=1, genreID=1),  # first_user likes Action
        GenrePref(userID=1, genreID=2),  # first_user also likes Adventure
        GenrePref(userID=2, genreID=3),  # another_user likes Puzzle
        GenrePref(userID=3, genreID=2),  # third_user likes Adventure
    ]
    test_session.add_all(genre_prefs)
    test_session.commit()

    # Create Wishlist entries
    wishlists = [
        Wishlist(userID=1, gameID=1),  # first_user wants Action Game 1
        Wishlist(userID=2, gameID=2),  # another_user wants Puzzle Game 1
        Wishlist(userID=3, gameID=3),  # third_user wants Adventure Game 1
    ]
    test_session.add_all(wishlists)
    test_session.commit()

    # Create Game Preferences
    game_prefs = [
        GamePref(userID=1, gameID=1),  # first_user prefers Action Game 1
        GamePref(userID=1, gameID=3),  # first_user also prefers Adventure Game 1
        GamePref(userID=2, gameID=2),  # another_user prefers Puzzle Game 1
        GamePref(userID=3, gameID=3),  # third_user prefers Adventure Game 1
    ]
    test_session.add_all(game_prefs)
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

    response = client.get("/user/first_user")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 2
    assert data == {"userID": 1, "username": "first_user"}
    
def test_get_wishlist(override_get_db, test_session): 
    populate_database(test_session)
    
    response = client.get("/user/first_user/wishlist")
    assert response.status_code == 200

    data = response.json()
    print(data)
    assert isinstance(data, list)
    assert data == [{'id': 1, 'gamename': 'Action Game 1', 'description': 'An exciting action-packed adventure.', 'genres': 'Action, Adventure'}]
    

def test_post_wishlist(override_get_db, test_session): 
    populate_database(test_session)
    wishlist_item = {
        "gameID": 123 
    }
    
    response = client.post("/user/first_user/wishlist", json=wishlist_item)
    
    assert response.status_code == 200 
    
    data = response.json()
    
    assert "message" in data
    assert data["message"] == "Game added to wishlist"
    assert "wishlist_entry" in data
    assert data["wishlist_entry"] == {"userID": 1, "gameID": 123}
    
    new_entry = test_session.query(Wishlist).filter_by(userID=1, gameID=123).first()
    assert new_entry is not None
    assert new_entry.userID == 1
    assert new_entry.gameID == 123

def test_remove_wishlist(override_get_db, test_session): 
    populate_database(test_session)

    response = client.delete("/user/first_user/wishlist/1")
    
    assert response.status_code == 200 
    
    data = response.json()
    
    assert "message" in data
    assert data["message"] == "Game removed from wishlist"
    assert "wishlist_entry" in data
    assert data["wishlist_entry"] == {"userID": 1, "gameID": 1}
    
def test_delete_wishlist(override_get_db, test_session): 
    populate_database(test_session)

    response = client.delete("/user/first_user/wishlist")
    
    assert response.status_code == 200 
    
    data = response.json()
    
    assert "message" in data
    assert data["message"] == "All games removed from wishlist"
    

def test_get_genrepref(override_get_db, test_session): 
    populate_database(test_session)
   
    response = client.get("/user/first_user/genrepref")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert data == ["Action", "Adventure"]  

def test_post_genrepref(override_get_db, test_session): 
    populate_database(test_session)
    
    entry = {
        "genrename": "Puzzle" 
    }
    
    response = client.post("/user/first_user/genrepref", json=entry)
    
    assert response.status_code == 200  
    
    data = response.json()
    assert "message" in data
    assert data["message"] == "Genre added"
    assert "Entry" in data
    assert data["Entry"] == {'genrename': "Puzzle", 'userID': 1}
    
    new_entry = test_session.query(GenrePref).filter_by(userID=1, genreID=2).first()
    assert new_entry is not None
    assert new_entry.userID == 1
    assert new_entry.genreID == 2

def test_remove_genrepref(override_get_db, test_session): 
    populate_database(test_session)
  
    response = client.delete("/user/first_user/genrepref/Action")
    
    assert response.status_code == 200  
    
    data = response.json()
    assert "message" in data
    assert data["message"] == "Genre removed from GenrePref"
    assert "removed" in data
    assert data["removed"] == {"userID": 1, "genrename": "Action"}
    
    removed_entry = test_session.query(GenrePref).filter_by(userID=1, genreID=1).first()
    assert removed_entry is None

def test_delete_all_genrepref(override_get_db, test_session): 
    populate_database(test_session)

    response = client.delete("/user/first_user/genrepref")
    
    assert response.status_code == 200  
    
    data = response.json()
    assert "message" in data
    assert data["message"] == "All genrePres removed from genrePref"
    
    remaining_prefs = test_session.query(GenrePref).filter_by(userID=1).all()
    assert len(remaining_prefs) == 0


def test_get_gampref(override_get_db, test_session): 
    populate_database(test_session)
    
    response = client.get("/user/first_user/gamepref")
    assert response.status_code == 200  

    data = response.json()
    assert isinstance(data, list) 
    print(data)
    assert data == [{'id': 1, 'gamename': 'Action Game 1', 'description': 'An exciting action-packed adventure.', 'genres': 'Action, Adventure'}, {'id': 3, 'gamename': 'Adventure Game 1', 'description': 'Explore and uncover secrets in this adventure game.', 'genres': 'Adventure'}]

def test_post_gamepref(override_get_db, test_session): 
    populate_database(test_session)
    new_game_pref = {"gameID": 2}  
    
    response = client.post("/user/first_user/gamepref", json=new_game_pref)
    assert response.status_code == 200  

    data = response.json()
    assert "message" in data
    assert data["message"] == "Game added"
    assert "Entry" in data
    assert data["Entry"] == {"userID": 1, "gameID": 2}

    new_entry = test_session.query(GamePref).filter_by(userID=1, gameID=3).first()
    assert new_entry is not None
    assert new_entry.userID == 1
    assert new_entry.gameID == 3

def test_remove_gamepref(override_get_db, test_session): 
    populate_database(test_session)
 
    response = client.delete("/user/first_user/gamepref/1")
    assert response.status_code == 200  

    data = response.json()
    assert "message" in data
    assert data["message"] == "Game removed from gamePref"
    assert "gamePref" in data
    assert data["gamePref"] == {"userID": 1, "gamePref": 1}

    removed_entry = test_session.query(GamePref).filter_by(userID=1, gameID=1).first()
    assert removed_entry is None

def test_delete_all_gamepref(override_get_db, test_session): 
    populate_database(test_session)
   
    response = client.delete("/user/first_user/gamepref")
    assert response.status_code == 200  

    data = response.json()
    assert "message" in data
    assert data["message"] == "All genrePres removed from GamePref"

    remaining_entries = test_session.query(GamePref).filter_by(userID=1).all()
    assert len(remaining_entries) == 0

class RecommendationBody(BaseModel):
    rows: list[dict]
@pytest.fixture
def mock_aiserver():
    async def mock_handler(request: httpx.Request):
        return httpx.Response(
            status_code=200,
            json={"games": [[1, 2, 3], [4, 5, 6]]}
        )
    transport = httpx.MockTransport(mock_handler)
    return transport

@pytest.mark.asyncio
async def test_post_recommendation(override_get_db, test_session, mock_aiserver):
    async def mock_http_client():
        async with httpx.AsyncClient(transport=mock_aiserver) as client:
            yield client

    app.dependency_overrides[get_http_client] = mock_http_client

    populate_database(test_session)

    recommendation_body = {
        "rows": [
            {"similar_to_games": [1, 2, 3]},
            {"similar_to_games": "all"},
            {"similar_to_genre": "Sports"},
            {"best_reviewed": "Adventure"},
            {"best_sales": "Action"}
        ]
    }

    response = client.post(
        "/user/first_user/recommendation",
        json=recommendation_body
    )

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "games" in data["response"]
