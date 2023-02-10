import bcrypt
from database.database import DatabaseConnection

initial_users = [
    {
        "name": "John Doe",
        "username": "johndoe",
        "email": "johndoes@email.com",
        "passwordHash": "secret",
        "resourcePosts": []
    },
    {
        "name": "Jane Doe",
        "username": "janedoe",
        "email": "janedoe@email.com",
        "passwordHash": "supersecret",
        "resourcePosts": []
    },
    {
        "name": "John Smith",
        "username": "johnsmith",
        "email": "smith@test.com",
        "passwordHash": "password",
        "resourcePosts": []
    },
]

initial_posts = [
    {
        "title": "First Post",
        "description": "This is the first post",
        "url": "https://www.google.com",
        "moduleName": "Python",
        "tags": ["python", "fastapi"],
        "semester": 2
    },
    {
        "title": "Second Post",
        "description": "This is the second post",
        "url": "https://www.google.com",
        "moduleName": "Python",
        "tags": ["python", "fastapi"],
        "semester": 2
    }
]

def insert_users(database: DatabaseConnection, user_documents: list[dict]):
    collection = database.db.get_collection("users")
    for user in user_documents:
        user = user.copy()
        password_hash: bytes = bcrypt.hashpw(
            bytes(user["passwordHash"], "utf-8"), bcrypt.gensalt()
        )
        user["passwordHash"] = password_hash.decode("utf-8")
        collection.insert_one(document=user)


def insert_posts(database: DatabaseConnection, post_documents: list[dict], user_for_post: dict):
    collection = database.db.get_collection("resourcePosts")
    user = database.db.get_collection("users").find_one(
        {"username": user_for_post["username"]}
        )
    for post in post_documents:
        post["user"] = user["_id"]
        collection.insert_one(document=post)