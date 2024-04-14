from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException

from app.config.db_dependency import DBSessionDep
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import  UserCreateSchema
from app.utils.hash import hash_password,verify_password

# async def get_user(db_session: AsyncSession, user_id: str) -> User:
#         result = await db_session.execute(select(User).where(User.id == user_id))
#         user = result.scalars().first()
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         return user


class UserService:

    def __init__(self, user_repository:UserRepository):
        self.user_repository=user_repository

    async def get_user_by_id(self, user_id: UUID) -> User:
        """Получить пользователя по ID."""
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
        
    async def create_user(self,user_data:UserCreateSchema)->User:
        user = User(
            username=user_data.username,
            slug = user_data.slug,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=hash_password(user_data.hashed_password)
        )
        new_user = await self.user_repository.add(user)
        return new_user

user_service = UserService(UserRepository(db_session=DBSessionDep,model=User))