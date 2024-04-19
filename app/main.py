from fastapi import FastAPI
import uvicorn
from routers.user import router as user_router
from routers.product import router as product_router
import logging
import sys
from contextlib import asynccontextmanager
from config.db import sessionmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


def create_app()->FastAPI:
    app = FastAPI(docs_url='/',lifespan=lifespan)
    app.include_router(router = user_router)
    app.include_router(router= product_router)
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000,reload=True)     