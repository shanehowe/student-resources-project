from fastapi import (
    APIRouter, 
    status, 
    HTTPException,
)
from fastapi.responses import JSONResponse
from utils.JWTHelper import JwtHelper
from models.user import UserLoginIn, UserLogin
from database.database import database
import bcrypt

login_router = APIRouter()

@login_router.post("/api/login", response_model=None)
def login(user: UserLoginIn) -> JSONResponse:
    collection = database.db.get_collection("users")
    found_user = collection.find_one({"username": user.username.strip().lower()})

    if not found_user:
        raise HTTPException(
            detail="incorrect username or password",
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user_indb = UserLogin(**found_user)
    password_isvalid = bcrypt.checkpw(
        bytes(user.password, "utf-8"),
        bytes(user_indb.passwordHash, "utf-8")
    )

    if not password_isvalid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="incorrect username or password"
        )
    
    token = JwtHelper.create_token(user_indb)
    return JSONResponse(
        status_code=200,
        content={"token": token, "username": user_indb.username, "name": user_indb.name}
        )

    
    
