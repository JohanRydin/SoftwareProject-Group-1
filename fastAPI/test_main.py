import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base, User, GenrePref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# test_main.py
from database import test_engine, get_test_db  # Assuming your test_engine is defined in database.py


# Test Database Setup
TEST_DATABASE_URL = "sqlite:///:memory:"  # In-memory SQLite database
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="module", autouse=True)
def setup_test_database():
    # Create tables in the in-memory SQLite database
    Base.metadata.create_all(bind=test_engine)

    # Override the app's get_db dependency
    app.dependency_overrides[get_db] = lambda: get_test_db() #TODO! Why does this not work later? 


    # Teardown: Drop tables after tests
    Base.metadata.drop_all(bind=test_engine)

# Use TestClient to simulate API requests
client = TestClient(app)

# Example test for POST /user/{username}/genrepref
def test_post_genrepref():
    # Arrange: Add a test user
    test_username = "testuser"
    with next(get_test_db()) as db:  # Extract session from the generator
        db.add(User(username=test_username))
        db.commit()
    


# Example test for POST /users/
def test_create_user():
    # Arrange: Create a new user payload
    test_username = "newuser"
    user_data = {"username": test_username}

    # Send a POST request to the /users/ endpoint with the user data
    response = client.post("/users/", json=user_data)

    # Assert: Check the response status code
    assert response.status_code == 200  # Or 201 if that's your response code for successful creation

    # Assert: Verify the user is returned correctly in the response
    response_data = response.json()
    assert "id" in response_data  # Assuming the User model has an `id` field
    assert response_data["username"] == test_username

    # Assert: Check if the user was actually added to the database
    with next(get_test_db()) as db:  # Get the session from the generator
        db_user = db.query(User).filter_by(username=test_username).first()
        assert db_user is not None
        assert db_user.username == test_username