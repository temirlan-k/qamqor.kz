from fastapi import Depends, FastAPI
from sqladmin import Admin
import uvicorn
from config.db_dependency import DBSessionDep
from services.admin import AdminAuth, get_admin_service
from models.admin import UserAdmin,ProductAdmin,CategoryAdmin
from routers.user import router as user_router
from routers.product import router as product_router
from routers.order import router as order_router

from contextlib import asynccontextmanager
from config.db import sessionmanager,get_db_session
from config.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

# def admin_config(app,engine):
#     authentication_backend = get_admin_service(get_db_session)  # This should return an instance of AdminAuth
#     admin = Admin(app=app ,authentication_backend=authentication_backend,engine=engine)
#     admin.add_view(UserAdmin)
#     admin.add_view(ProductAdmin)
#     admin.add_view(CategoryAdmin)
#     return admin



def create_app() -> FastAPI:
    app = FastAPI(docs_url="/", lifespan=lifespan)
    # admin_config(app,sessionmanager._engine)
    app.include_router(router=user_router)
    app.include_router(router=product_router)
    app.include_router(router=order_router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
