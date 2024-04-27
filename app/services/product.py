import json
from typing import List
from uuid import UUID

import aioredis
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from utils.decarators.cache_decarator import cache_redis
from config.redis import get_redis_connection
from schemas.product import CreateProductIn, ProductOutDB,ProductInDB
from config.db_dependency import DBSessionDep
from repositories.product_repo import ProductProtocol, ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository, redis: aioredis.Redis):
        self.product_repository = product_repository
        self.redis = redis

    @cache_redis(key_prefix="product",cache_type='details', expire=10)
    async def get_product_by_id(self, product_id: UUID) -> ProductInDB:
        product = await self.product_repository.select_product_by_id(product_id)
        return product
    
    @cache_redis(key_prefix='products',cache_type='list',expire=10)
    async def get_all_products(self,category):
        products = await self.product_repository.select_all_products(category)
        return products

    async def create_product(self,product_data: CreateProductIn,seller_id:str):
        new_product = await self.product_repository.insert_product(product_data,seller_id)
        return new_product

    



async def get_product_service(db: DBSessionDep) -> ProductService:
    try:
        product_repository: ProductProtocol = ProductRepository(db)
        redis = await get_redis_connection()
        return ProductService(product_repository, redis)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create UserService: {str(e)}"
        )
