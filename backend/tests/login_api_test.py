from main import app
from fastapi.testclient import TestClient
from database.database import database
from tests.api_helper import initial_users, insert_users
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
    database.db.users.delete_many({})
    user = initial_users[0]
    insert_users(database, [user])
    yield database
    database.db.users.delete_many({})
    database.client.close()


def test_valid_login(connect):
    user = initial_users[0]
    data_for_login = {
        "username": user["username"],
        "password": user["passwordHash"]
    }
    response = client.post("/api/login", json=data_for_login)
    token_data = response.json()
    assert response.status_code == 200
    assert token_data["token"] is not None
    assert token_data["username"] == user["username"]
    assert token_data["name"] == user["name"]


def test_invalid_login(connect):
    bad_data = {
        "username": "I dont exist",
        "password": "Neither do I!!"
    }
    response = client.post("/api/login", json=bad_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "incorrect username or password"
