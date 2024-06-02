import json

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


def test_delete_user_by_body_success():
    user_data = {"name": "John Doe", "email": "johndoe@example.com"}
    response = client.post("/users", json=user_data)

    user_delete_data = {"user_id": "1"}
    delete_response = client.request("DELETE", "/users", content=json.dumps(user_delete_data))
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "User deleted successfully"}


def test_delete_user_by_body_not_found():
    user_delete_data = {"user_id": 999}
    response = client.request("DELETE", "/users", content=json.dumps(user_delete_data))
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
