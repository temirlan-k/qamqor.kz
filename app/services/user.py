from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import  UserCreateIn, UserLoginIn
from utils.hash import hash_password,verify_password



class UserService:

    def __init__(self, user_repository:UserRepository):
        self.user_repository=user_repository

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Get user by user id"""
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_user_by_id(self, email: str) -> User:
        """Get user by user email"""
        user = await self.user_repository.get_by_email(email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_all_users(self)->List[User]:
        """Get all users"""
        users = await self.user_repository.get_all_users()
        return users
        
    async def create_user(self,user_data:UserCreateIn)->User:
        """Create new user"""
        new_user = await self.user_repository.add_user(user_data)
        return new_user
    


    async def login_user(self,login_dto:UserLoginIn):
        """Login user"""
        user = await self.user_repository.get_by_id(login_dto.id)




        

    
async def get_user_service(db: DBSessionDep) -> UserService:
    try:
        user_repository = UserRepository(db)
        return UserService(user_repository)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create UserService: {str(e)}")
