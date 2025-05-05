import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_signup():
    response = client.post("/user/signup", json={"username": "testuser", "email": "testsemail"})
    data = response.json()
    assert response.status_code == 200 or response.status_code == 400 or response.status_code == 422    assert "username" in data
    assert data["username"] == "testuser"
