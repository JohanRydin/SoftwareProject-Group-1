import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from sqlmodel import Session, SQLModel, create_engine, Field
from models import User, GenrePref  # Make sure these are imported


class User(SQLModel, table=True):
    __tablename__ = "user"  # Optional if you want to specify a table name

    userID: int = Field(primary_key=True)
    username: str = Field(index=True, unique=True)
    
    
# Use TestClient to simulate API requests
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Root url"}

def test_get_users(): 
    # Set up a test SQLite database
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
        #users = [User(userID=2, username="another_user"),User(userID=3, username="third_user"),]
        #session.add_all(users)
        #session.commit()
        
        # Test the actual API endpoint
        response = client.get("/users")  # Ensure the endpoint is correct

        # Clear the dependency override after the test
        app.dependency_overrides.clear()
        
        # Check the response
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)  # Check if the response is a list
        assert len(data) == 3  # Check if there are any users returned
