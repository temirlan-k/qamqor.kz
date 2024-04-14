import uuid
from sqlalchemy import UUID, Column
from sqlalchemy.orm import Mapped, mapped_column

from . import Base



class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)    
    username: Mapped[str] = mapped_column(index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    hashed_password: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=False)