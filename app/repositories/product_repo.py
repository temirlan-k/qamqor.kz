from typing import Protocol,Optional,List
from uuid import UUID

from fastapi import HTTPException
from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
class ProductProtocol(Protocol):

    async def get_product_by_id(self, id: str) -> Optional[Product]:
        raise NotImplementedError()

    async def get_all_products(self)->Product:
        raise NotImplementedError()
    
    async def add_product(self,user_data:Product)->Product:
        raise NotADirectoryError()
    

class ProductRepository:

    
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def get_product_by_id(self,id:UUID):
        stmt = await self.db_session.execute(select(Product).filter(Product.id == id))
        res = stmt.scalars().first()
        if res is None:
            raise HTTPException(status_code=404,detail="Product not found") 
        return res
    
        
    