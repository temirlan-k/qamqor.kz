import json
import aioredis
from typing import List
from uuid import UUID
from fastapi import Depends, HTTPException,status

from config.redis import get_redis_connection
from utils.decarators.cache_decarator import cache_redis
from auth.auth_bearer import JWTBearer
from auth.auth_handler import decodeJWT, signJWT
from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserProtocol, UserRepository
from schemas.user import UserCreateIn, UserLoginIn
from utils.hash import verify_password


class UserService:

    def __init__(self, user_repository: UserRepository , redis:aioredis.Redis ):
        self.user_repository = user_repository
        self.redis = redis 
    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get user by user id"""
        user = await self.user_repository.select_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")


        return user

    async def get_user_by_email(self, email: str) -> User:
        """Get user by user email"""
        user = await self.user_repository.select_user_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_all_users(self) -> List[User]:
        """Get all users"""
        users = await self.user_repository.select_all_users()
        return users

    async def create_user(self, user_data: UserCreateIn) -> dict:
        """Create new user"""
        new_user = await self.user_repository.insert_user(user_data)
        return signJWT(new_user.id, new_user.username)

    @cache_redis(key_prefix='user',expire=30)
    async def get_current_user(self, token: str = Depends(JWTBearer())) -> dict:
        payload = decodeJWT(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token, user ID missing.",
            )

        user = await self.user_repository.select_user_by_id(str(user_id))
        return user.to_dict()

    async def login_user(self, login_dto: UserLoginIn) -> dict:
        """Login user"""
        user = await self.user_repository.select_by_username_or_email(
            login_dto.username_or_email
        )
        if user and verify_password(login_dto.password, user.hashed_password):
            return signJWT(user.id, user.username)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username, email, or password",
            )


async def get_user_service(db: DBSessionDep) -> UserService:
    try:
        user_repository:UserProtocol = UserRepository(db)
        redis = await get_redis_connection()
        return UserService(user_repository,redis)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create UserService: {str(e)}"
        )
