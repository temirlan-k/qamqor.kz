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

class ProductOutDB(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category_id: int
    category_name:str

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'category_name':self.category_name
        }


