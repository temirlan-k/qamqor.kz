from typing import Optional, Type, Generic, TypeVar, List
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from utils.hash import hash_password
from models.user import User
from schemas.user import UserCreateIn
from sqlalchemy import insert, or_
from sqlalchemy.exc import SQLAlchemyError
from typing import Protocol



class UserProtocol(Protocol):

    async def select_user_by_id(self, id: UUID) -> Optional[User]:
        ...

    async def select_user_by_email(self, email: str) -> Optional[User]:
        ...

    async def select_all_users(self) -> Optional[User]:
        ...

    async def insert_user(self, user_data: User) -> User:
        ...

    async def check_user_exist(self, username_or_email: str)-> bool:
        ...
    
class UserRepository(UserProtocol):

    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def check_user_exist(self, username_or_email: str) -> bool:
        stmt = await self.db_session.execute(
            select(User).where(
                or_(User.username == username_or_email, User.email == username_or_email)
            )
        )
        return stmt.scalars().first() is not None

    async def select_by_username_or_email(self, username_or_email: str)->Optional[User]:
        stmt = await self.db_session.execute(
            select(User).where(
                (User.username == username_or_email) | (User.email == username_or_email)
            )
        )
        res = stmt.scalars().first()
        if res is None:
            raise HTTPException(status_code=404, detail="User not found")
        print(res)
        return res

    async def select_user_by_id(self, id: UUID)-> Optional[User]:
        stmt = await self.db_session.execute(select(User).filter(User.id == id))
        res = stmt.scalars().first()
        if not res:
            raise HTTPException(status_code=404, detail="User not found")
        return res

    async def select_user_by_email(self, email: str) -> Optional[User]:
        stmt = await self.db_session.execute(select(User).filter(User.email == email))
        res = stmt.scalars().first()
        if not res:
            raise HTTPException(status_code=404, detail="User not found")
        return res

    async def select_all_users(self) -> Optional[User]:
        stmt = await self.db_session.execute(select(User))
        res = stmt.scalars().all()
        return res

    async def insert_user(self, user_data: User) -> User:
        if await self.check_user_exist(
            username=user_data.username, email=user_data.email
        ):
            raise HTTPException(status_code=400, detail="User already exist")

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
            raise HTTPException(status_code=400, detail=str(e))
        return new_user
