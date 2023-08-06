import pytest
from fastapi.testclient import TestClient
from main import app
import database, crud
from logger import logger

client = TestClient(app)

@pytest.fixture
def db_session():
    session = next(database.get_db())
    session = database.local_session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture(autouse=True)
def setup_test_data(db_session):
    # Clean up any existing data and ensure a fresh state for each test
    # db_session.query(models.StorageObject).delete()
    
    for user in crud.get_users(db_session):
        db_session.delete(user)
        
    for group in crud.get_groups(db_session):
        db_session.delete(group)
        
    db_session.commit()
    
    # Create a testuser for relevant tests
    response = client.post("/users/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200

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
    assert response.json() == "running"

# Test exception handler for PermissionError
def test_permission_exception_handler():
    response = client.get("/users/me")
    print(response.json())
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

# Test exception handler for ValueError
def test_valueerror_exception_handler():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.post("/storage/directory", json={"name": "invalid", "path": "invalid"}, headers=headers)
    print(response)
    assert response.status_code == 400
    assert "Oopsie!" in response.json()["message"]

# Test user creation endpoint
def test_create_user():
    response = client.post("/users/", json={"username": "newuser", "password": "newpassword"})
    assert response.status_code == 200
    assert "username" in response.json()[0]

# Test user deletion endpoint
def test_delete_user():
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.delete("/users/", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()

def upload_file(token, path, content):
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post(
        "/storage/file",
        headers=headers,
        files={"file": ("test.txt", content.decode())},  # Encode the content as bytes
        data={"path": path},
    )
    return response

def test_upload_file():
    # Create user1
    response = client.post("/users/", json={"username": "user1", "password": "password1"})
    assert response.status_code == 200
    user1 = response.json()[0]
    token1 = response.json()[1]

    # Authenticate as user1 and upload a file
    content_user1 = b"Hello, User1!"
    path_user1 = "/"
    response = upload_file(token1, path_user1, content_user1)
    print("response", response)
    assert response.status_code == 200

    # ... rest of the test code ...

def test_share_with_user():
    # Create user1
    response = client.post("/users/", json={"username": "user1", "password": "password1"})
    assert response.status_code == 200
    user1 = response.json()[0]
    token1 = response.json()[1]

    # Authenticate as user1 and upload a file
    content_user1 = b"Hello, User1!"
    path_user1 = "/user1-files/"
    response = upload_file(token1, path_user1, content_user1)
    assert response.status_code == 200

    # ... rest of the test code ...




# Test sharing with group
def test_share_with_group():
    # Create a user1
    response = client.post("/users/", json={"username": "user1", "password": "password1"})
    assert response.status_code == 200
    user1 = response.json()[0]
    token1 = response.json()[1]

    # Authenticate as user1 and upload a file
    headers1 = {"Authorization": f"Bearer {token1}"}
    response = client.post("/storage/file", headers=headers1, files={"file": ("test.txt", "Hello, User1!")}, data={"path": "/user1-files/"})
    assert response.status_code == 200

    # Create a group
    response = client.post("/groups/", headers=headers1, json={"group_name": "group1"})
    assert response.status_code == 200

    # Share the file with the group
    response = client.post("/shares/group", headers=headers1, json={"group_name": "group1", "path": "/user1-files/test.txt", "permission": "RW"})
    assert response.status_code == 200

    # Authenticate as user1 again and check if the file is visible in the shared group
    response = client.get("/groups/me", headers=headers1)
    assert response.status_code == 200
    assert "/user1-files/test.txt" in response.json()["shared"][0]["children"]

    # Create another user2
    response = client.post("/users/", json={"username": "user2", "password": "password2"})
    assert response.status_code == 200
    user2 = response.json()[0]
    token2 = response.json()[1]

    # Authenticate as user2 and check if the shared file is visible
    headers2 = {"Authorization": f"Bearer {token2}"}
    response = client.get("/storage/", headers=headers2)
    assert response.status_code == 200
    assert "/user1-files/test.txt" in response.json()["owned_objects"]["children"]



# Add more test cases for other endpoints as needed.
# Remember to cover different scenarios, error cases, etc.

if __name__ == "__main__":
    pytest.main()
