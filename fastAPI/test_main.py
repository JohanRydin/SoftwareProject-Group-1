import pytest
from fastapi.testclient import TestClient
from main import app, get_db
from models import Base, User, GenrePref
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  


# Use TestClient to simulate API requests
client = TestClient(app)


