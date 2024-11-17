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