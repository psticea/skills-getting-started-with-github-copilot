import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_and_unregister():
    activity = "Chess Club"
    email = "testuser@mergington.edu"
    # Ensure user is not already signed up
    client.post(f"/activities/{activity}/unregister?email={email}")
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

def test_signup_duplicate():
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/unregister?email={email}")
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    client.post(f"/activities/{activity}/unregister?email={email}")

def test_unregister_not_signed_up():
    activity = "Chess Club"
    email = "notregistered@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
