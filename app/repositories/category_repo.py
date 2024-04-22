from typing import Protocol, Optional, List
from uuid import UUID
from fastapi import HTTPException
from models.category import Category
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class CategoryProtocol(Protocol):
    
    async def select_category_by_id(self,id:UUID)->Optional[Category]:
        ...

    async def select_all_categories(self)->Category:
        ...

    async def insert_category(self,category:Category)->Category:
        ...


class CategoryRepository:

    def __init__(self,db_session:AsyncSession) -> None:
        self.db_session = db_session   

    
    async def select_category_by_id(self,id:UUID)->Optional[Category]:
        stmt = await self.db_session.execute(select(Category).where(Category.id==id))
        res = stmt.scalars().first()
        if res is None:
            raise HTTPException(status_code=404,detail='Category not found')
        return res
    
    async def select_all_categories(self)->Category:
        stmt = await self.db_session.execute(select(Category))
        res = stmt.scalars().all()
        return res
    
    async def insert_category(self,category:Category)->Category:
        new_category = Category(
            name=category.name
        )
        self.db_session.add(new_category)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(new_category)
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return new_category

