from uuid import UUID
import aioredis
from fastapi import HTTPException
from schemas.order import OrderCreate
from config.redis import get_redis_connection
from config.db_dependency import DBSessionDep
from repositories.order_repo import OrderProtocol, OrderRepository


class OrderService:
    
    def __init__(self, order_repository: OrderRepository, redis: aioredis.Redis):
        self.order_repository = order_repository
        self.redis = redis

    async def create_order(self, order_create: OrderCreate, id: UUID):
        order = await self.order_repository.insert_order(order_create, id)
        return order


async def get_order_service(db: DBSessionDep) -> OrderService:
    try:
        order_repository: OrderProtocol = OrderRepository(db)
        redis = await get_redis_connection()
        return OrderService(order_repository, redis)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to create UserService: {str(e)}"
        )