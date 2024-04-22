import datetime
import time
import sqlalchemy as sa
import enum
from typing import TYPE_CHECKING
from sqlalchemy import orm as so
import uuid


from . import Base


if TYPE_CHECKING:
    from .category import Category
    from .user import User
    from .product import Product


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: so.Mapped[uuid.UUID] = so.mapped_column(
        default=uuid.uuid4, primary_key=True, index=True, unique=True
    )
