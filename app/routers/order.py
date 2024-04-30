from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, File, Form,Query, UploadFile

from models.category import Category
from auth.auth_bearer import JWTBearer
from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.order import OrderCreate
from services.order import OrderService, get_order_service
from services.user import UserService, get_user_service

router = APIRouter()

@router.post('/order/create',tags=['orders',],dependencies=[Depends(JWTBearer())])
async def create_order(order_create: OrderCreate,
                       user_service: UserService = Depends(get_user_service),
                       order_service:OrderService = Depends(get_order_service),
                       token:str = Depends(JWTBearer())):
    
    current_user = await user_service.get_current_user(token)
    return await order_service.create_order(order_create, current_user.get('id'))
    