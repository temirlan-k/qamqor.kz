from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException

from auth.auth_bearer import JWTBearer
from auth.auth_handler import decodeJWT, signJWT
from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import  UserCreateIn, UserLoginIn
from utils.hash import hash_password,verify_password
from fastapi import status


class UserService:

    def __init__(self, user_repository:UserRepository):
        self.user_repository=user_repository

    async def get_user_by_id(self, user_id: str) -> User:
        """Get user by user id"""
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_user_by_email(self, email: str) -> User:
        """Get user by user email"""
        user = await self.user_repository.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_all_users(self)->List[User]:
        """Get all users"""
        users = await self.user_repository.get_all_users()
        return users
        
    async def create_user(self,user_data:UserCreateIn)->dict:
        """Create new user"""
        new_user = await self.user_repository.add_user(user_data)
        return signJWT(new_user.id,new_user.username)
    


    async def get_current_user(self, token: str) -> dict:
        payload = decodeJWT(token)
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid token, user ID missing.')

        user = await self.user_repository.get_by_id(str(user_id))
        return {
            **user.__dict__
        }



    async def login_user(self,login_dto:UserLoginIn)->dict:
        """Login user"""
        user = await self.user_repository.get_user_by_username_or_email(login_dto.username_or_email)
        if user and verify_password(login_dto.password,user.hashed_password):
            return signJWT(user.id, user.username)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username, email, or password"
            )




        

    
async def get_user_service(db: DBSessionDep) -> UserService:
    try:
        user_repository = UserRepository(db)
        return UserService(user_repository)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create UserService: {str(e)}")
