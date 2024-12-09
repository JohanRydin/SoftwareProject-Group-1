import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base, User, GenrePref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  

# Use TestClient to simulate API requests
client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Root url"}
    
    
def test_get_users(): 
    response = client.get("http://localhost:8000/user/Erik")
    data = response.json()
    assert response.status_code == 200 #Success code 
    
    