import uuid
from typing import TYPE_CHECKING, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from . import Base

if TYPE_CHECKING:
    from .product import Product


class User(Base):
    __tablename__ = "users"
    id = sa.Column(
        sa.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    username: so.Mapped[str] = so.mapped_column(index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(index=True, unique=True)
    first_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    hashed_password: so.Mapped[str]
    is_verified: so.Mapped[bool] = so.mapped_column(default=False)

    products: so.Mapped[List["Product"]] = so.relationship(
        back_populates="user", cascade="all,delete-orphan"
    )

    def to_dict(self):
        return{
            'id':str(self.id),
            'username':self.username,
            'email':self.email,
            'first_name':self.first_name,
            'last_name':self.last_name,
            'is_verified':self.is_verified,
        }
    
