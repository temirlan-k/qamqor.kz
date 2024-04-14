from abc import ABC,abstractmethod
from typing import Type, Generic, TypeVar, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app import models

T = TypeVar('T', bound=models.Base)

class SQLRepository(ABC,Generic[T]):
    def __init__(self,db_session:AsyncSession,model:Type[T]) -> None:
        self.db_session = db_session
        self.model = model

    @abstractmethod
    async def get_by_id(self,id:str)->T:
        ...

    @abstractmethod
    async def add(self,user_data:User)->T:
        ...

    @abstractmethod
    async def update(self,user_data:User)->T:
        ...



