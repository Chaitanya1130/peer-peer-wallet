import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_signup():
    response = client.post("/user/signup", json={"username": "testuser", "email": "testsemail"})
    data = response.json()
    assert response.status_code == 200 or response.status_code == 400 or response.status_code == 422

    if response.status_code == 200:
        assert "username" in data
        assert data["username"] == "testuser"
    elif response.status_code == 400 or response.status_code == 422:
        assert "detail" in data
        assert isinstance(data["detail"], list)
        assert len(data["detail"]) > 0
        password_error_found = False
        for error in data["detail"]:
            if error.get("loc") == ["body", "password"] and error.get("msg") == "Field required":
                password_error_found = True
                break
        assert password_error_found