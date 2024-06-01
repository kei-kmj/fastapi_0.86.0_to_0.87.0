import pytest
from fastapi.testclient import TestClient
from main import app
from models import UserModel

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # テストの前にユーザーデータをリセット
    UserModel.users = []
    UserModel.id_counter = 1
    yield
    # テストの後にもユーザーデータをリセット
    UserModel.users = []
    UserModel.id_counter = 1


def test_get_users_empty():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []


def test_create_user():
    user_data = {"name": "John Doe", "email": "johndoe@example.com"}
    response = client.post("/users", json=user_data)
    assert response.status_code == 200
    user = response.json()
    assert user["name"] == "John Doe"
    assert user["email"] == "johndoe@example.com"
    assert "id" in user


def test_get_users():
    user_data = {"name": "John Doe", "email": "johndoe@example.com"}
    client.post("/users", json=user_data)
    response = client.get("/users")
    assert response.status_code == 200
    users = response.json()
    assert len(users) == 1
    assert users[0]["name"] == "John Doe"
    assert users[0]["email"] == "johndoe@example.com"


def test_delete_user():
    user_data = {"name": "John Doe", "email": "johndoe@example.com"}
    response = client.post("/users", json=user_data)
    user_id = response.json()["id"]
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "User deleted successfully"}

    get_response = client.get("/users")
    assert get_response.status_code == 200
    assert get_response.json() == []


def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_by_body_success():
    user_data = {"name": "John Doe", "email": "john@example.com"}
    response = client.post("/users", json=user_data)
    user_id = response.json()["id"]

    user_delete_data = {"user_id": user_id}
    delete_response = client.delete("/users", json=user_delete_data)
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "User deleted successfully"}


def test_delete_user_by_body_not_found():
    user_delete_data = {"user_id": 999}
    response = client.delete("/users", json=user_delete_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

