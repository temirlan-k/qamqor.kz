from fastapi import HTTPException
from sqladmin import Admin, ModelView
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from models.user import User
from utils.hash import verify_password
from config.db_dependency import DBSessionDep
from repositories.user_repo import UserProtocol, UserRepository
from config.settings import settings
import random
import secrets
import string
from datetime import datetime, timedelta
from typing import Protocol, Optional, List
from uuid import UUID
from fastapi import HTTPException
from models.category import Category
from models.product import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select



def generate_session_token():
    token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    return token

class AdminAuth(AuthenticationBackend):
    
    def __init__(self,secret_key, db_session:AsyncSession):
        self.db_session = db_session
        super().__init__(secret_key=secret_key)

    async def select_by_username_or_email(self, username_or_email: str) -> User:
        stmt = select(User).where((User.username == username_or_email) | (User.email == username_or_email))
        result = await self.db_session.execute(stmt)  
        user = result.scalars().first() 
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user



    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        
        user = await self.select_by_username_or_email(username)
        print(user)
        if user and  verify_password(password,user.hashed_password):
            token = generate_session_token()
            expiry_date = datetime.now() + timedelta(hours=2) 
            request.session.update({"token": token, "expiry_date": expiry_date})
            return True
        
        return False
    
    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        expiry_date = request.session.get("expiry_date")
        
        if not token or datetime.now() > expiry_date:
            return False
        return True




def get_admin_service(db) -> AdminAuth:
    return AdminAuth(secret_key=settings.SECRET_KEY,db_session=db)
   

