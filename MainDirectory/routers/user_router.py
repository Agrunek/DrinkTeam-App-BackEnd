# user_router.py
from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from pydantic import BaseModel
from MainDirectory.services.user_service import UserService

user_router = APIRouter(
    prefix="/user",
    tags=["users"]
)

SECRET_KEY = "secret_key"  #TODO: hide !!
ACCESS_TOKEN_EXPIRE_MINUTES = 30#minutes 

fake_db = {} # TODO: remove
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# TODO: replace with db entry
class User(BaseModel):
    username: str
    password: str


def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str: #returns token
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")


def get_current_user(token: str = Depends(UserService.verify_token)) -> str: #returns username
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username not in fake_db:
            raise HTTPException(status_code=401, detail="Invalid token")
        return fake_db.get(username)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=str(e))


@user_router.post("/register")
def register(user: User):
    if user.username in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = pwd_context.hash(user.password)
    fake_db[user.username] = {"username": user.username, "password": hashed_password}
    return {"msg": "User registered successfully"}


@user_router.post("/login")
def login(user: User):
    stored_user = fake_db.get(user.username)
    if not stored_user or not pwd_context.verify(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_jwt_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.post("/refresh")
def refresh_token(current_user: dict = Depends(get_current_user)):
    access_token = create_jwt_token({"sub": current_user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}


# example of route that requires JWT
@user_router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {"msg": f"Hello, {current_user['username']}"}
