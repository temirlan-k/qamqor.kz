from typing import Protocol, Optional, List
from uuid import UUID
from fastapi import HTTPException
from models.category import Category
from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class ProductProtocol(Protocol):

    async def select_product_by_id(self, id: UUID) -> Optional[Product]:
        ...

    async def select_product_by_category(self,category_id:UUID)->Optional[Product]:
        ...

    async def select_all_products(self) -> Product:
        ...

    async def insert_product(self, user_data: Product,seller_id:UUID) -> Product:
        ...


class ProductRepository(ProductProtocol):


    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def select_product_by_id(self, id: UUID) -> Optional[dict]:
        stmt =  await self.db_session.execute(
            select(Product, Category.name.label('category_name'))
            .join(Category, Product.category_id == Category.id)
            .filter(Product.id == id)
        )
        product_tuple = stmt.first()
        print(product_tuple[0])
        if product_tuple is None:
            raise HTTPException(status_code=404, detail="Product not found")
        product, category_name = product_tuple  
        product_data = {
        
            "id": str(product.id),
            "category_id": str(product.category_id),
            "user_id": str(product.user_id),
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "picture": product.picture,
            "created_at": product.created_at,
            "update_time": product.update_time,
            "category_name": category_name
        }

        return product_data

    async def select_product_by_category(self,category_id:List[UUID])->Optional[Product]:
        stmt = await self.db_session.execute(select(Product).where(Product.category_id==category_id))
    
    async def select_all_products(self,category:str) -> List[Product]:
        stmt = select(Product, Category.name).join(Category, Product.category_id == Category.id)
        result = await self.db_session.execute(stmt)
        products_with_categories = []
        for product, category_name in result:
            product_dict = {
                "id": str(product.id),
                "category_id": str(product.category_id),
                "user_id": str(product.user_id),
                "name": product.name,
                "description": product.description,
                "price": product.price,  
                "picture": product.picture,
                "created_at": product.created_at,
                "update_time": product.update_time,
                "category_name": category_name,
            }
            products_with_categories.append(product_dict)
        return products_with_categories


    async def insert_product(self, product_data: Product,seller_id:UUID)-> Product:
        new_product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            picture=product_data.picture,
            category_id=product_data.category_id,
            user_id = seller_id
        )   
        self.db_session.add(new_product)
        try:
            await self.db_session.commit()
            await self.db_session.refresh(new_product)
        except Exception as e:
            await self.db_session.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return new_product


            
