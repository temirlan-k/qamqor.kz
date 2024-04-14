import time
from typing import Dict
from fastapi import HTTPException
import jwt
from app.config.settings import settings


def token_response(access:str,)-> Dict[str]:
    return {
        'access':access,
        
    }


def signJWT(user_id:str,username:str):
    payload={
        'sub':user_id,
        'username':username,
        'exp':time.time() + 600
    }
    jwt = jwt.encode(payload,settings.SECRET_KEY,settings.HASHING_ALGORITHM)
    return token_response(jwt)


def decodeJWT(token:str):
    try:
        decoded_token = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
        return decoded_token if decoded_token['exp']>=time.time() else None
    except:
        return {}
    
