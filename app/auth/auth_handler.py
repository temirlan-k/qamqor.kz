import time
from typing import Dict
from fastapi import HTTPException,status
import jwt
from config.settings import settings


def token_response(access:str):
    return {'access':access}


def signJWT(user_id:str,username:str):
    payload={
        'sub':str(user_id),
        'username':username,
        'exp':time.time() + 600
    }
    access_token = jwt.encode(payload,settings.SECRET_KEY,settings.HASHING_ALGORITHM)
    return token_response(access_token)


def decodeJWT(token: str):
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.HASHING_ALGORITHM)
        if decoded_token['exp'] < time.time():
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except jwt.JWTError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"JWT Error: {str(e)}")
    
