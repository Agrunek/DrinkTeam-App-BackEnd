# user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm

from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from app.services.user_service import UserService
from app.database.database import get_session
from app.schemas.user_schema import LoginRequest, RegisterRequest, UpdateRequest
from app.models.user import User
import json


user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



@user_router.post("/register")
def register(user: RegisterRequest, db : _orm.Session = Depends(get_session)):
    try:
        if UserService.get_user_by_email(db, user.email):
            raise HTTPException(status_code=400, detail="Email already in use")
        hashed_password = pwd_context.hash(user.password)
        UserService.create_user(db, user, hashed_password)
    except Exception as e:
        return {"msg": str(e)}

    return {"msg3": "User registered successfully"}


def is_email(text:str):
    return '@' in text

@user_router.post("/login")
def login(user: LoginRequest, db : _orm.Session = Depends(get_session)):
    try:
        if is_email(user.username_or_email):
            email = user.username_or_email
            stored_user: User = UserService.get_user_by_email(db, email)
            username = stored_user.username
        else: #username given instead
            username = user.username_or_email
            stored_user: User = UserService.get_user_by_username(db, username)
            email = stored_user.email

        if not stored_user or not pwd_context.verify(user.password, stored_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        access_token = UserService.create_jwt_token({"sub": email})

    except Exception as e:
        return {"msg": str(e)}
    return {"access_token": access_token, "token_type": "bearer"}



@user_router.post("/refresh")
def refresh_token(user_email: str = Depends(UserService.get_current_user)):
    access_token = UserService.create_jwt_token({"sub": user_email})
    return {"access_token": access_token, "token_type": "bearer"}





# example of route that requires JWT
@user_router.get("/protected")
def protected_route(user_email: str = Depends(UserService.get_current_user)):
    return {"msg": f"Hello, {user_email}"}
