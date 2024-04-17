from uuid import UUID
from fastapi import APIRouter, Depends

from config.db_dependency import DBSessionDep
from models.user import User
from repositories.user_repo import UserRepository
from schemas.user import  UserCreateOut, UserCreateIn
from services.user import  UserService, get_user_service

router = APIRouter()


@router.get("/user/{user_id}")
async def read_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    """Get User by Id"""
    return await user_service.get_user_by_id(user_id)

@router.get("/users")
async def read_users(user_service: UserService = Depends(get_user_service)):
    """Get All Users"""
    return await user_service.get_all_users()


@router.post('/user/create',response_model=UserCreateOut)
async def register(user_data:UserCreateIn,user_service:UserService = Depends(get_user_service)):
    """Create New User"""
    return await user_service.create_user(user_data)

