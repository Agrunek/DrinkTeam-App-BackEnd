from pydantic import BaseModel
from datetime import datetime

class ReviewResponse(BaseModel):
    comment : str
    rating : int
    creation_date : datetime
    recipe_id : int
    user_id : int

    model_config = {
        "from_attributes": True
    }


class ReviewRequestAdd(BaseModel):
    comment : str
    rating : int
    recipe_id : int
    user_id : int

    model_config = {
        "from_attributes": True
    }
