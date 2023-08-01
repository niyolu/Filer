import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def get_access_token():
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    return response.json()["access_token"]

# Test login endpoint
def test_login():
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

# Test authenticated endpoint (example: /users/me)
def test_authenticated_endpoint():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()
    # Add more assertions based on the expected response for this endpoint.

# Test unauthenticated endpoint (example: /)
def test_unauthenticated_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "running"

# Test exception handler for PermissionError
def test_permission_exception_handler():
    response = client.get("/some-protected-endpoint")
    assert response.status_code == 403
    assert "Oopsie!" in response.json()["message"]

# Test exception handler for ValueError
def test_valueerror_exception_handler():
    response = client.post("/some-endpoint", data={"param1": "invalid"})
    assert response.status_code == 400
    assert "Oopsie!" in response.json()["message"]

# Test user creation endpoint
def test_create_user():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/users/", json={"username": "newuser", "password": "newpassword"}, headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()

# Test user deletion endpoint
def test_delete_user():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete("/users/", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()

# Test upload file endpoint
def test_upload_file():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    file_content = b"some file content"
    response = client.post("/storage/file", files={"file": ("test.txt", file_content)}, data={"path": "/test"}, headers=headers)
    assert response.status_code == 200
    assert "name" in response.json()

# Add more test cases for other endpoints as needed.
# Remember to cover different scenarios, error cases, etc.

if __name__ == "__main__":
    pytest.main()
