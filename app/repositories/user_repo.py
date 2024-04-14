
from abc import ABC,abstractmethod
from typing import Type, Generic, TypeVar, List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app import models
from app.repositories.base import SQLRepository
from sqlalchemy.exc import SQLAlchemyError



class UserRepository(SQLRepository[User]):


    async def get_by_id(self, id: str) -> User:
        async with self.db_session as session:
            result = await session.execute(select(self.model).filter(self.model.id == id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404,detail="User not found") 
            return user

    async def add(self,user_data:User)->User:
        async with self.db_session as session:
            try:
                print(user_data.email)
                session.add(user_data)
                await session.commit()
                await session.refresh(user_data)
                return user_data
            except SQLAlchemyError as e:
                await session.rollback()
                print(e)
                raise e
            
    async def update(self,id:str,user_data:User)->User:
        async with self.db_session as session:
            stmt = select(User).filter_by(User.id == id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            if user is None:
                raise HTTPException(status_code=404,detail='User not found')

            