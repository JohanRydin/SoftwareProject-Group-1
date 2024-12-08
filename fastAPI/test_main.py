import pytest
from fastapi.testclient import TestClient
from main import app, get_test_db

# Use TestClient to simulate API requests
client = TestClient(app)


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client

# Example test for a POST endpoint
def test_post_genrepref():
    username = "testuser"
    genre_id = 1
    response = client.post(f"/user/{username}/genrepref", params={"genreID": genre_id})
    assert response.status_code == 200 or response.status_code == 400
    if response.status_code == 200:
        assert response.json()["message"] == "Genre added"
    elif response.status_code == 400:
        assert response.json()["detail"] == "Game is already in the genrePref"
