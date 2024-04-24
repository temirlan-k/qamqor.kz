import datetime
import sqlalchemy as sa
from typing import TYPE_CHECKING, List
from sqlalchemy import orm as so
from uuid import uuid4, UUID


from . import Base
from .order_product_association import order_product_association_table


if TYPE_CHECKING:

    from .category import Category
    from .user import User
    from .order import Order


class Product(Base):
    __tablename__ = "products"

    id: so.Mapped[UUID] = so.mapped_column(
        default=uuid4, primary_key=True, unique=True, index=True
    )
    category_id: so.Mapped[UUID] = so.mapped_column(sa.ForeignKey("category.id"))
    user_id: so.Mapped[UUID] = so.mapped_column(sa.ForeignKey("users.id"))
    name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=False)
    price: so.Mapped[float] = so.mapped_column()
    picture: so.Mapped[str] = so.mapped_column()

    created_at: so.Mapped[datetime.datetime] = so.mapped_column(
        server_default=sa.func.now(), default=datetime.datetime.now
    )
    update_time: so.Mapped[datetime.datetime] = so.mapped_column(
        server_default=sa.func.now(), server_onupdate=sa.func.now()
    )

    category: so.Mapped["Category"] = so.relationship(
        "Category", back_populates="products"
    )
    user: so.Mapped["User"] = so.relationship("User", back_populates="products")
    orders: so.Mapped[List["Order"]] = so.relationship(
        secondary=order_product_association_table, back_populates="products"
    )
    def to_dict(self):
        return {
            "id": str(self.id),
            "category_id": str(self.category_id),
            "category_name":str(self.category.name),
            "user_id": str(self.user_id),
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "picture": self.picture,
            "created_at": str(self.created_at),
            "update_time": str(self.update_time),
        }