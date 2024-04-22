from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends,Query

from models.category import Category
from auth.auth_bearer import JWTBearer
from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.product import CreateProductIn
from services.product import ProductService, get_product_service
from services.user import UserService, get_user_service

router = APIRouter()


@router.get("/product/{product_id}", dependencies=[Depends(JWTBearer())], tags=["products"])
async def fetch_product_by_id(product_id: UUID, product_service: ProductService = Depends(get_product_service)):
    """Get Product by Id"""
    return await product_service.get_product_by_id(product_id)

@router.get("/products")
async def fetch_product_by_categories(cat:List[str] = Query(None),product_service: ProductService = Depends(get_product_service)):
    """"""
    return cat

@router.post("/product/create", dependencies=[Depends(JWTBearer())], tags=["products"])
async def create_product(product_data: CreateProductIn,current_user: UserService = Depends(get_user_service),
                         product_service: ProductService = Depends(get_product_service),token=Depends(JWTBearer()) ):
    
    product_seller = await current_user.get_current_user(token)
    created_product = await product_service.create_product(product_data,product_seller.get('id'))

    return created_product

