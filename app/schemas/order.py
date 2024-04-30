from pydantic import BaseModel, UUID4
from typing import List

class ProductOrder(BaseModel):
    product_id: UUID4
    quantity: int

class OrderCreate(BaseModel):
    products: List[ProductOrder]
    contact_phone_number: str
    address: str
    promo_code: str | None

class OrderDisplay(BaseModel):
    id: UUID4
    total_price: float
    status: str
    products: List[ProductOrder] 
