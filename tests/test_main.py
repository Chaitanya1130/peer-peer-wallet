from fastapi.testclient import TestClient
from wallet import app


client=TestClient(app)
def test_user_signup():
    response = client.post("/user/signup",json={"username":"testuser","email":"testsemail","password":"testpass"})
    data=response.json()
    assert response.status_code == 200 or response.status_code == 400
    assert "username" in data
    assert data["username"] == "testuser"