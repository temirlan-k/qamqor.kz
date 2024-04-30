from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form,Query, UploadFile

from models.category import Category
from auth.auth_bearer import JWTBearer
from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.product import CreateProductIn, ProductOutDB
from services.product import ProductService, get_product_service
from services.user import UserService, get_user_service

router = APIRouter()


@router.get("/product/{product_id}", dependencies=[Depends(JWTBearer())], tags=["products"])
async def fetch_product_by_id(product_id: UUID, product_service: ProductService = Depends(get_product_service)):
    """Get Product by Id"""
    return await product_service.get_product_by_id(id=product_id)

@router.get("/products",tags=['products'])
async def fetch_all_products(category:list[str] = Query(None),product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_all_products(category)


@router.post("/product/create", dependencies=[Depends(JWTBearer())], tags=["products"])
async def create_product(
    name: str = Form(...), 
    description: str = Form(...),
    price: float = Form(...),
    category_id: str = Form(...),
    quantity:int = Form(...),
    file: UploadFile = File(...),
    current_user: UserService = Depends(get_user_service),
    product_service: ProductService = Depends(get_product_service),
    token = Depends(JWTBearer())
):
    product_data = CreateProductIn(name=name, description=description, price=price,quantity=quantity,category_id=category_id)
    product_seller = await current_user.get_current_user(token)
    created_product = await product_service.create_product(product_data, product_seller.get('id'), file)

    return created_product

@router.get('/products/me', dependencies=[Depends(JWTBearer())],tags=["products"])
async def fetch_user_products(product_service: ProductService = Depends(get_product_service),
                              current_user: UserService = Depends(get_user_service),
                              token=Depends(JWTBearer())):
    
    seller_id = await current_user.get_current_user(token)
    products = await product_service.get_user_products(id=seller_id.get('id'))
    return products

