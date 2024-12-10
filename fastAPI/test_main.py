import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlmodel import Session, SQLModel, create_engine, Field
from models import User, GenrePref  # Make sure these are imported
import os

class User(SQLModel, table=True):
    __tablename__ = "user"  # Optional if you want to specify a table name

    userID: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    
# File path for the test database
TEST_DB_PATH = "testing.db"

def clean_test_db():
    """Remove the testing.db file to ensure the database is clean before each test."""
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

# Use TestClient to simulate API requests
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Root url"}

def test_get_users(): 
    # Set up a test SQLite database
    clean_test_db()


    engine = create_engine("sqlite:///testing.db", connect_args={"check_same_thread": False})

    # Create all tables in the test database, ensure models are imported first
    SQLModel.metadata.create_all(engine)  # This will create the User and other tables

    # Create a session to interact with the test database
    with Session(engine) as session:
        
        # Override the get_db dependency to use the test session
        def get_db_override():
            return session
        
        app.dependency_overrides[get_db] = get_db_override
        #print("Tables created:", SQLModel.metadata.tables)
        # Insert test data into the database (add a user)
         # Insert test data into the database (add a user)
        users = [
            User(userID=1, username="first_user"),
            User(userID=2, username="another_user"),
            User(userID=3, username="third_user"),
        ]
        session.add_all(users)
        session.commit()
        
        # Test the actual API endpoint
        response = client.get("/users")  # Ensure the endpoint is correct

        # Clear the dependency override after the test
        app.dependency_overrides.clear()
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)  # Check if the response is a list
        assert len(data) == 3  # Check if there are any users returned
        assert data[0] == {"userID": 1, "username": "first_user"}

