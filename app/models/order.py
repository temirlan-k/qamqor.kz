from datetime import datetime
import uuid
import enum
from typing import TYPE_CHECKING, List
import sqlalchemy as sa
import sqlalchemy.orm as so
from . import Base
from .order_product_association import order_product_association_table


if TYPE_CHECKING:

    from .product import Product


class ORDER_STATUS_ENUM(enum.Enum):
    PENDING = "PENDING"
    IN_SHIPPING_CENTER = "IN_SHIPPING_CENTER"
    IN_DELIVERY = "IN_DELIVERY"
    COMPLETED = "COMPLETED"


class Order(Base):
    __tablename__ = "orders"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        primary_key=True, unique=True, index=True, default=uuid.uuid4
    )
    user_id: so.Mapped[uuid.UUID] = so.mapped_column(sa.ForeignKey("users.id"))
    total_price: so.Mapped[float] = so.mapped_column()
    contact_phone_number: so.Mapped[str] = so.mapped_column()
    address: so.Mapped[str] = so.mapped_column()
    status: so.Mapped[enum.Enum] = so.mapped_column(
        sa.Enum(ORDER_STATUS_ENUM, name="order_status_enum")
    )
    promo_code: so.Mapped[str | None]
    created_at: so.Mapped[datetime] = so.mapped_column(
        server_default=sa.func.now(), default=datetime.now
    )

    products: so.Mapped[List["Product"]] = so.relationship(
        secondary=order_product_association_table, back_populates="orders"
    )

    def to_dict(self):
        return {
            'id':self.id,
            'user_id':str(self.user_id),
            'total_price':self.total_price,
            'contact_phone_number':self.contact_phone_number,
            'address':self.address,
            'status':self.status,
            'created_at':self.created_at
        }