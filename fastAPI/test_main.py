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
    
    
# Define the test database path
TEST_DB_PATH = "testing.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_PATH}"

# Clean up the test database before running tests
def clean_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

# Reusable database engine for tests
@pytest.fixture(scope="function")
def test_engine():
    clean_test_db()
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)  # Create tables for all models
    yield engine
    clean_test_db()  # Cleanup after test

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

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Root url"}

def test_get_users(override_get_db, test_session):
    # Insert test data into the database
    users = [
        User(userID=1, username="first_user"),
        User(userID=2, username="another_user"),
        User(userID=3, username="third_user"),
    ]
    test_session.add_all(users)
    test_session.commit()

    # Test the API endpoint
    response = client.get("/users")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0] == {"userID": 1, "username": "first_user"}