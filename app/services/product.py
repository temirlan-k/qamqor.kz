import json
from uuid import UUID

import aioredis
from fastapi import HTTPException
from utils.decarators.cache_decarator import cache_redis
from config.redis import get_redis_connection
from schemas.product import CreateProductIn, ProductInDB
from config.db_dependency import DBSessionDep
from repositories.product_repo import ProductProtocol, ProductRepository


class ProductService:
    def __init__(self, product_repository: ProductRepository, redis: aioredis.Redis):
        self.product_repository = product_repository
        self.redis = redis

    @cache_redis(key_prefix="product", expire=10)
    async def get_product_by_id(self, product_id: UUID) -> ProductInDB:
        product = await self.product_repository.select_product_by_id(product_id)
        if not product:
            return None

        return product.to_dict()

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
