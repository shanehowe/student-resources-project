from fastapi import APIRouter, HTTPException, status
from models.user import PyObjectId, UserIn, UserOut
from database.database import database
import bcrypt
from typing import Any

user_router = APIRouter()


@user_router.get("/")
def index():
    return {"Ping": "Pong"}


@user_router.get("/api/users", response_model=None)
def get_users() -> list[UserOut]:
    """
    Returns all users found in users collection
    """
    collection = database.db.users
    users = collection.find()
    return [UserOut(**user) for user in users]


@user_router.get("/api/users/{id}", response_model=None)
def get_user(id: PyObjectId) -> UserOut:
    """
    Returns user with specified id
    Raises 404 not found if cannot find id
    """
    collection = database.db.get_collection("users")
    user = collection.find_one({"_id": id})

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not exist"
        )

    return UserOut(**user)


@user_router.post("/api/users", status_code=status.HTTP_201_CREATED, response_model=None)
def create_user(user: UserIn) -> UserOut:
    user.email = user.email.lower().strip()
    user.username = user.username.strip().lower()
    user.name = user.name.strip().title()
    collection = database.db.get_collection("users")
    existing_username = collection.find_one({"username": user.username})
    existing_email = collection.find_one({"email": user.email})

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Username has been taken. Choose a new one",
        )
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="There is an account associated with this email already.",
        )
    # validate password length
    if not (len(user.username) > 3 and len(user.password) > 3):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="username and password must be longer than 3 charactors",
        )

    password_hash: bytes = bcrypt.hashpw(
        bytes(user.password, "utf-8"), bcrypt.gensalt()
    )
    document: dict[str, Any] = {
        "name": user.name,
        "username": user.username,
        "passwordHash": password_hash.decode("utf-8"),
        "email": user.email,
        "resourcePosts": [],
    }
    created_user_id = collection.insert_one(document=document).inserted_id
    created_user = collection.find_one({"_id": PyObjectId(created_user_id)})
    response = UserOut(**created_user) # type: ignore
    return response


@user_router.delete("/api/users/{id}", response_model=None)
def delete_user(id: PyObjectId):
    ...
