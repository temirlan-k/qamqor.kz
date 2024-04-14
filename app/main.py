from fastapi import FastAPI
import uvicorn
from app.routers.user import router as user_router

import logging
import sys
from contextlib import asynccontextmanager
from app.config.db import sessionmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


def create_app()->FastAPI:
    app = FastAPI(docs_url='/',lifespan=lifespan)
    app.include_router(router = user_router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8000,reload=True)     