from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends,Header
from auth.auth_bearer import JWTBearer
from config.db_dependency import DBSessionDep
from models.user import User

from repositories.user_repo import UserRepository
from schemas.user import UserCreateOut, UserCreateIn, UserLoginIn,UserOut
from services.user import UserService, get_user_service

router = APIRouter()

@router.post("/user/register", tags=["auth"])
async def register(
    user_data: UserCreateIn, user_service: UserService = Depends(get_user_service)
):
    """Create New User"""
    return await user_service.create_user(user_data)


@router.post("/user/login", tags=["auth"])
async def login(
    user_data: UserLoginIn, user_service: UserService = Depends(get_user_service)
):
    """Login User"""
    return await user_service.login_user(user_data)


@router.get("/user/{user_id}", tags=["users"])
async def read_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    """Get User by Id"""
    return await user_service.get_user_by_id(user_id)


@router.get("/users", tags=["users"],response_model=List[UserOut])
async def read_users(user_service: UserService = Depends(get_user_service))->List[UserOut]:
    """Get All Users"""
    return await user_service.get_all_users()


@router.get("/me", dependencies=[Depends(JWTBearer())], tags=["users"])
async def read_current_user(
    user_service: UserService = Depends(get_user_service),
    token: str = Depends(JWTBearer()),
):
    return await user_service.get_current_user(token)


@router.post('/verify-account')
async def verify_account(user_service: UserService = Depends(get_user_service),token: str = Header(None)):
    return await user_service.verify_account(token)