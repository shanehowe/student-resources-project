from main import app
from fastapi.testclient import TestClient
from database.database import database
from tests.api_helper import insert_users, initial_users
from dotenv import load_dotenv
import pytest
import os
load_dotenv(".env")

MONGO_URI = os.getenv("DEV_MONGO_URI")
TEST_DATABASE_NAME = os.getenv("TEST_DATABASE")
client = TestClient(app)

@pytest.fixture(scope="module")
def connect():
    database.connect(MONGO_URI, TEST_DATABASE_NAME)
    insert_users(database, initial_users)
    yield database
    database.db.users.delete_many({})
    database.client.close()


def test_root(connect):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Ping": "Pong"}


def test_get_users(connect):
    response = client.get("/api/users")
    assert response.status_code == 200
    assert len(response.json()) == len(initial_users)
    assert response.json()[0]["username"] == initial_users[0]["username"]


def test_get_user_by_id(connect):
    users = database.db.users.find()
    user = users[0]
    response = client.get(f"/api/users/{user['_id']}")
    assert response.status_code == 200
    assert response.json()["username"] == user["username"]
    

def test_sensitive_info_is_not_sent(connect):
    users = database.db.users.find()
    user = users[0]
    response = client.get(f"/api/users/{user['_id']}")
    assert response.status_code == 200
    assert "passwordHash" not in response.json()
    assert "email" not in response.json()
    assert "username" in response.json()
    assert "_id" in response.json()


def test_get_user_by_id_not_found(connect):
    response = client.get("/api/users/5f5a4b4a4c4b4b4b4b4b4b4b")
    assert response.status_code == 404
    assert response.json() == {"detail": "user not exist"}


def test_create_user(connect):
    user = {
        "username": "superuser",
        "email": "superuser@test.com",
        "password": "superuser",
        "name": "Super User"
    }
    response = client.post("/api/users", json=user)
    assert response.status_code == 201
    assert response.json()["username"] == user["username"]
    created_user = database.db.users.find_one({"username": user["username"]})
    assert created_user is not None


def test_create_user_with_existing_username(connect):
    user = {
        "username": initial_users[0]["username"],
        "email": "differenttotherest@email.com",
        "password": "superuser",
        "name": "Super User"
    }
    response = client.post("/api/users", json=user)
    assert response.status_code == 422
    assert response.json()["detail"] == "Username has been taken. Choose a new one"


def test_create_user_with_existing_email(connect):
    user = {
        "username": "differenttotherest",
        "email": initial_users[0]["email"],
        "password": "superuser",
        "name": "Super User"
    }
    response = client.post("/api/users", json=user)
    assert response.status_code == 422
    assert response.json()["detail"] == "There is an account associated with this email already."


def test_create_user_invalid_username(connect):
    user = {
        "username": "ab",
        "email": "hello@bye.ie",
        "password": "abcd",
        "name": "Super User"
    }
    response = client.post("/api/users", json=user)
    detail = response.json()["detail"]
    assert response.status_code == 422
    assert detail == "username and password must be longer than 3 charactors"


def test_create_user_invalid_password(connect):
    user = {
        "username": "abcdefgh",
        "email": "hello123@bye.ie",
        "password": "d",
        "name": "Super User"
    }
    response = client.post("/api/users", json=user)
    detail = response.json()["detail"]
    assert response.status_code == 422
    assert detail == "username and password must be longer than 3 charactors"