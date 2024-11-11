from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
import fastapi as _fastapi

from MainDirectory.services.user_service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

@user_router.get("/login")
def get_test():
    return UserService.get_test()