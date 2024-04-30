from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):

    name: str
    description: str
    price: float


class CreateProductIn(BaseModel):
    name: str
    description: str
    price: float
    quantity:int
    category_id: UUID


class ProductInDB(ProductBase):
    id: UUID
    created_at: str
    update_time: str

    class Config:
        from_attributes = True


class ProductOutDB(BaseModel):
    id:str
    name: str
    description: str
    price: float
    picture: str
    quantity:int
    category_name: str
    created_at: str

    class Config:
        from_attributes = True

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "picture": self.picture,
            "category_name": self.category_name,
            "created_at-": self.created_at
        }
