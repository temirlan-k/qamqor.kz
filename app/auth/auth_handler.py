import time
from typing import Dict
from fastapi import HTTPException, status
import jwt
from config.settings import settings


def token_response(access: str)->dict:
    return {"access": access}


def signJWT(user_id: str, username: str)->dict:
    payload = {"sub": str(user_id), "username": username, "exp": time.time() + settings.ACCESS_TOKEN_LIFETIME}
    access_token = jwt.encode(payload, settings.SECRET_KEY, settings.HASHING_ALGORITHM)
    return token_response(access_token)


def decodeJWT(token: str)->dict:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=settings.HASHING_ALGORITHM
        )
        if decoded_token["exp"] < time.time():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
        )