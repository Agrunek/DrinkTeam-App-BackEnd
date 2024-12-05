import jwt
from sqlalchemy import func as func_time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime
from pydantic import BaseModel
from datetime import datetime, timedelta
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from app.models.user import User
from app.schemas.user_schema import RegisterRequest, LoginRequest, UpdateRequest
from app.database.database import get_session
import json

SECRET_KEY = None
with open("./app/password.json", "r") as file:
    SECRET_KEY = json.load(file)['SECRET_JWT_KEY']

ACCESS_TOKEN_EXPIRE_MINUTES = 30#minutes 
security = HTTPBearer()

class UserService:
    
    @staticmethod
    def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            token = credentials.credentials
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = payload.get("sub")
            
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
            return token
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    @staticmethod
    def create_jwt_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str: #returns token
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def get_user_by_email(db: _orm.Session, email):
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: _orm.Session, username):
        return db.query(User).filter(User.username == username).first()
    
    
    @staticmethod
    def create_user(db, request: RegisterRequest, hashed_password):
        user = User(username = request.username, 
                    email = request.email, 
                    password = hashed_password, 
                    date_of_birth = request.date_of_birth,
                    creation_date = func_time.now())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update_user(db, request: UpdateRequest, pwd_context, user_email):
        user = db.query(User).filter(User.email == user_email).first()

        update_data = request.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            if field == "password":
                value = pwd_context.hash(value)
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_current_user(db: _sql.orm.Session = Depends(get_session), token: str = Depends(verify_token)):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            email = payload.get("sub")
            user = UserService.get_user_by_email(db, email)
            if user is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return user.email
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.PyJWTError as e:
            raise HTTPException(status_code=401, detail=str(e))