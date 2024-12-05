from pydantic import BaseModel
from datetime import datetime

class UserResponse(BaseModel):
    user_id : int
    username : str
    email : str
    date_of_birth : datetime
    creation_date : datetime

    model_config = {
        "from_attributes": True
    }



class LoginRequest(BaseModel):
    username_or_email : str | None
    password: str

    model_config = {
        "from_attributes": True
    }


class RegisterRequest(BaseModel):
    username : str
    email : str
    password: str
    date_of_birth : datetime

    model_config = {
        "from_attributes": True
    }

class UpdateRequest(BaseModel):
    user_id : int
    username : str | None
    email : str | None
    date_of_birth : datetime | None

    model_config = {
        "from_attributes": True
    }
