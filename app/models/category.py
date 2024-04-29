from typing import TYPE_CHECKING, List
import sqlalchemy as sa
from sqlalchemy import orm as so
from uuid import uuid4, UUID


from . import Base

if TYPE_CHECKING:
    from .product import Product


class Category(Base):
    __tablename__ = "category"

    id: so.Mapped[UUID] = so.mapped_column(
        default=uuid4, primary_key=True, unique=True, index=True
    )
    name: so.Mapped[UUID] = so.mapped_column(sa.String(255), nullable=False)

    products: so.Mapped[List["Product"]] = so.relationship(
        back_populates="category", cascade="all,delete-orphan"
    )
