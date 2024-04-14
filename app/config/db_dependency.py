from typing import Annotated

from app.config.db import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]