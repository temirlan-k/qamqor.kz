from uuid import UUID
from fastapi import APIRouter, Depends

from app.config.db_dependency import DBSessionDep
from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.schemas.user import  UserCreateSchema
from app.services.user import  UserService

router = APIRouter()

def get_user_service(db:DBSessionDep)-> UserService:
    return UserService(UserRepository(db,User))

@router.get("/user/{user_id}")
async def read_user(user_id: UUID, user_service: UserService = Depends(get_user_service)):
    """Get User by Id"""
    return await user_service.get_user_by_id(user_id)

@router.post('/user/create')
async def register(user_data:UserCreateSchema,user_service:UserService = Depends(get_user_service)):
    """Create New User"""
    return await user_service.create_user(user_data)