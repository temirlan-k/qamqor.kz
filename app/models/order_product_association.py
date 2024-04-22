from __future__ import annotations
from . import Base
from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import Integer
from sqlalchemy.orm import relationship


order_product_association_table = Table(
    "order_product_association",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("order_id", ForeignKey("orders.id"), nullable=False),
    Column("product_id", ForeignKey("products.id"), nullable=False),
    UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
)