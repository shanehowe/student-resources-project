from main import app
from fastapi.testclient import TestClient
from database.database import database
from tests.api_helper import insert_users, initial_users, initial_posts, insert_posts
from models.pyobjectId import PyObjectId
from typing import Any
from dotenv import load_dotenv
import pytest
import os

load_dotenv(".env")

MONGO_URI = os.getenv("DEV_MONGO_URI")
TEST_DATABASE_NAME = os.getenv("TEST_DATABASE")
client = TestClient(app)

def get_token_header(user: dict) -> dict[str, Any]:
    """
    initial_users[0] will own all the posts in testing database
    use this for when a token is required to perform an action

    for testing when a user doesnt own the post 
    use initial_users[1]
    """
    json_data = {
        "username": user["username"],
        "password": user["passwordHash"]
    }
    response = client.post("/api/login", json=json_data)
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def get_user_from_post(post: dict[str, Any]) -> dict:
    id = post["user"]["_id"]
    user = database.db.users.find_one({"_id": PyObjectId(id)})
    return user


@pytest.fixture(scope="module")
def connect():
    database.connect(MONGO_URI, TEST_DATABASE_NAME)
    insert_users(database, initial_users)
    insert_posts(database, initial_posts, initial_users[0])
    yield database
    database.db.users.delete_many({})
    database.db.resourcePosts.delete_many({})
    database.client.close()


def test_get_resources(connect):
    response = client.get("/api/resources")
    assert response.status_code == 200
    assert len(response.json()) == len(initial_posts)


def test_get_resource_by_id(connect):
    post_indb = database.db.resourcePosts.find_one({"title": initial_posts[0]["title"]})
    id = post_indb["_id"]
    response = client.get(f"api/resources/{id}")
    assert response.status_code == 200
    assert response.json()["title"] == post_indb["title"]


def test_creating_valid_resource(connect):
    header = get_token_header(initial_users[0])
    post = {
        "title": "Programming in Python",
        "description": "Getting started with Python",
        "semester": 2,
        "tags": ["programming"],
        "moduleName": "Programming",
        "url": "www.fakeurl.com"
    }
    response = client.post("/api/resources", json=post, headers=header)
    created_post = response.json()
    user_indb = get_user_from_post(created_post)
    assert response.status_code == 201
    assert created_post["user"] is not None
    assert user_indb["_id"] == user_indb["_id"]


def test_users_post_list_is_updated(connect):
    header = get_token_header(initial_users[0])
    post = {
        "title": "Programming in Python",
        "description": "Getting started with Python",
        "semester": 2,
        "tags": ["programming"],
        "moduleName": "Programming",
        "url": "www.fakeurl.com"
    }
    response = client.post("/api/resources", json=post, headers=header)
    created_post = response.json()
    user_indb = get_user_from_post(created_post)
    assert response.status_code == 201
    assert PyObjectId(created_post["_id"]) in user_indb["resourcePosts"]


def test_creating_post_without_token(connect):
    post = {
        "title": "Programming in Python",
        "description": "Getting started with Python",
        "semester": 2,
        "tags": ["programming"],
        "moduleName": "Programming",
        "url": "www.fakeurl.com"
    }
    response = client.post("/api/resources", json=post)
    detail = response.json()["detail"]
    assert response.status_code == 401 # Unauthorized!
    assert detail == "Missing token"


def test_create_post_mssing_fields(connect):
    headers = get_token_header(initial_users[0])
    # Post is missing moduleName and title
    bad_post = {
        "description": "Getting started with Python",
        "semester": 2,
        "tags": ["programming"],
        "url": "www.fakeurl.com"
    }
    response = client.post("/api/resources", json=bad_post, headers=headers)
    json_response = response.json()
    first_missing_msg = json_response["detail"][0]
    second_missing_msg = json_response["detail"][1]
    assert response.status_code == 422
    assert "title" in first_missing_msg["loc"]
    assert first_missing_msg["msg"] == "field required"
    assert "moduleName" in second_missing_msg["loc"]
    assert second_missing_msg["msg"] == "field required"
    

def test_updating_post(connect):
    headers = get_token_header(initial_users[0])
    post = {
        "title": "Programming in Python",
        "description": "Getting started with Python",
        "semester": 2,
        "tags": ["programming"],
        "moduleName": "Programming",
        "url": "www.fakeurl.com"
    }
    initial_response = client.post("/api/resources", json=post, headers=headers)
    post_id = initial_response.json()["_id"]
    modified_post = post.copy()
    modified_post["title"] = "Programming in Java!"
    response = client.put(f"/api/resources/{post_id}", json=modified_post, headers=headers)
    modified_title = response.json()["title"]
    post_indb = database.db.resourcePosts.find_one({"title": modified_title})
    assert response.status_code == 200
    assert post_indb is not None


def test_deleting_post(connect):
    posts_indb = database.db.resourcePosts.find({})
    post = posts_indb[0]
    headers = get_token_header(initial_users[0])
    response = client.delete(f"/api/resources/{post['_id']}", headers=headers)
    assert response.status_code == 200


def test_deleting_post_that_doesnt_belong_touser(connect):
    bad_header = get_token_header(initial_users[1])
    posts_indb = database.db.resourcePosts.find({})
    post = posts_indb[0]
    response = client.delete(f"/api/resources/{post['_id']}", headers=bad_header)
    assert response.status_code == 401
    assert response.json() == {
        "detail":"This action is only allowed by the owner of the post"
        }