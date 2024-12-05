# user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm

from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from app.services.user_service import UserService
from app.database.database import get_session
from app.schemas.user_schema import LoginRequest, RegisterRequest, UpdateRequest, UserGet
from app.models.user import User
import json


user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




@user_router.get("/")
def protected_route(db : _orm.Session = Depends(get_session), user_email: str = Depends(UserService.get_current_user)):
    user: User = UserService.get_user_by_email(db, user_email)

    response = UserGet(
        user_id = user.user_id,
        email = user.email,
        username = user.username,
        date_of_birth = user.date_of_birth 
    )
    return response


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



def fetch_user(db: _orm.Session, username_or_email):
    if '@' in username_or_email:
        return UserService.get_user_by_email(db, username_or_email)
    else:
        return UserService.get_user_by_username(db, username_or_email)


@user_router.post("/login")
def login(user: LoginRequest, db: _orm.Session = Depends(get_session)):
    try:

        stored_user: User = fetch_user(db, user.username_or_email)
        if not stored_user or not pwd_context.verify(user.password, stored_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        access_token = UserService.create_jwt_token({"sub": stored_user.email})
    except Exception as e:
        return {"msg": str(e)}

    return {"access_token": access_token, "token_type": "bearer"}




@user_router.get("/refresh")
def refresh_token(user_email: str = Depends(UserService.get_current_user)):
    access_token = UserService.create_jwt_token({"sub": user_email})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.put("/update")
def update_user(request: UpdateRequest, db: _orm.Session = Depends(get_session), user_email: str = Depends(UserService.get_current_user)):

    try:
        if user_email != request.email and UserService.get_user_by_email(db, request.email):
            raise HTTPException(status_code=400, detail="Email already in use")
       
        UserService.update_user(db, request, pwd_context, user_email)
    except Exception as e:
        return {"msg": str(e)}
    return {"msg": "User updated successfully"}



# example of route that requires JWT
@user_router.get("/protected")
def protected_route(user_email: str = Depends(UserService.get_current_user)):
    return {"msg": f"Hello, {user_email}"}
