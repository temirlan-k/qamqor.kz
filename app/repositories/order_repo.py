from typing import Protocol
from uuid import UUID
import aioredis
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.order import OrderCreate
from models.product import Product
from models.order_product_association import order_product_association_table
from models.order import ORDER_STATUS_ENUM, Order

class OrderProtocol(Protocol):

    async def insert_order(self, user_data: Order,buyer_id:UUID) -> Order:
        ...
    

class OrderRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def insert_order(self, order_create: OrderCreate, buyer_id: UUID):
            new_order = Order(
                user_id=buyer_id,
                contact_phone_number=order_create.contact_phone_number,
                address=order_create.address,
                promo_code=order_create.promo_code,
                status="PENDING",
                total_price = 0.0,
                
            )
            self.db_session.add(new_order)

            total_price = 0.0
            for product_order in order_create.products:
                product = await self.db_session.execute(
                    select(Product).where(Product.id == product_order.product_id)
                )
                product = product.scalar_one_or_none()

                if product and product.quantity >= product_order.quantity:
                    total_price += product.price * product_order.quantity
                    product.quantity -= product_order.quantity
                    new_order.quantity += product_order.quantity

                    association = order_product_association_table.insert().values(
                        order_id=new_order.id,
                        product_id=product.id,
                    )
                    await self.db_session.execute(association)
                else:
                    await self.db_session.rollback()
                    raise HTTPException(status_code=400, detail="Insufficient product stock")

            new_order.total_price = total_price

            await self.db_session.commit()
            return new_order