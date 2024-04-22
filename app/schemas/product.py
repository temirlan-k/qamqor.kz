from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):

    name: str
    description: str
    price: float
    picture: str


class CreateProductIn(ProductBase):
    category_id: UUID


class ProductInDB(ProductBase):
    id: UUID
    created_at: str
    update_time: str

    class Config:
        from_attributes = True