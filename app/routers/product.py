from uuid import UUID
from fastapi import APIRouter, Depends

from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import  UserCreateOut, UserCreateIn
from services.product import  ProductService, get_product_service

router = APIRouter()


@router.get("/product/{product_id}")
async def read_user(product_id: UUID, product_service: ProductService = Depends(get_product_service)):
    """Get Product by Id"""
    return await product_service.get_product_by_id(product_id)
