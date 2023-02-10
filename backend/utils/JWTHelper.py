from jose import jwt, JWTError, ExpiredSignatureError # type: ignore
from models.user import UserLogin
from dotenv import load_dotenv
from fastapi import HTTPException, status
import time
import os

load_dotenv(".env")
class JwtHelper:
    _algorithm: str = os.getenv("JWT_ALGO")
    _secret: str = os.getenv("JWT_SECRET")

    @classmethod
    def create_token(self, user: UserLogin) -> str:
        expires_in = round(time.time()) + (60 * 60) # Fix this
        to_encode = {
            "username": user.username,
            "name": user.name,
            "id": str(user.id),
            "exp": expires_in
        }    
        token = jwt.encode(
            to_encode,
            self._secret,
            self._algorithm
        )

        return token
    
    @classmethod
    def decode_token(self, token: str) -> dict[str, str]:
        try:
            payload = jwt.decode(token, self._secret, algorithms=[self._algorithm])
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token has expired"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="could not validate credentials"
            )
        return payload

