
from typing import Optional, Type, Generic, TypeVar, List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.hash import hash_password
from models.user import User
from schemas.user import UserCreateIn
from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError
from typing import  Protocol


class UserProtocol(Protocol):

    async def get_user_by_id(self, id: str) -> Optional[User]:
        raise NotImplementedError()
    
    async def get_by_email(self,email:str)-> Optional[User]:
        raise NotImplementedError()

    async def get_all_users(self)->User:
        raise NotImplementedError()
    
    async def add_user(self,user_data:User)->User:
        raise NotADirectoryError()
    


class UserRepository:

    def __init__(self,db_session: AsyncSession) -> None:
        self.db_session = db_session


    async def check_user_exist(self,username:str,email:str)-> bool:
        stmt = await self.db_session.execute(select(User).where(User.username == username or User.email == email))
        res = stmt.scalars().first() is not None
        return res


    async def get_by_id(self, id: str) -> User:
        stmt = await self.db_session.execute(select(User).filter(User.id==id))
        res = stmt.scalars().first()
        if not res:
             raise HTTPException(status_code=404,detail="User not found") 
        return res 

    async def get_by_email(self, email: str) -> User:
        stmt = await self.db_session.execute(select(User).filter(User.email==email))
        res = stmt.scalars().first()
        if not res:
             raise HTTPException(status_code=404,detail="User not found") 
        return res 


    async def get_all_users(self)->List[User]:
        stmt = await self.db_session.execute(select(User))
        res = stmt.scalars().all()
        return res
    

    async def add_user(self,user_data: UserCreateIn)->User:
        if await self.check_user_exist(username=user_data.username,email=user_data.email):
            raise HTTPException(status_code=400,detail='User already exist')
        
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hash_password(user_data.hashed_password),
        )
        self.db_session.add(new_user)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(new_user)
        except SQLAlchemyError as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=400,detail=str(e))
        return new_user

    