from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, List
from MainDirectory.schemas.category_schema import CategoryResponse
from MainDirectory.schemas.recipe_detail_schema import RecipeDetailResponse, RecipeDetailRequestAdd
from MainDirectory.schemas.user_schema import UserResponse

class RecipeRequestAdd(BaseModel):
    recipe_id : Optional[int] = None
    name : str
    image_url : Optional[str] = None
    preparation_time : time
    category_id : int
    recipe_detail : RecipeDetailRequestAdd
    user_id : int


class RecipeResponse(BaseModel):
    recipe_id : int
    name : str
    image_url : Optional[str] = None
    preparation_time : time
    creation_time : datetime
    last_modified : datetime
    category : CategoryResponse
    recipe_detail : RecipeDetailResponse
    user : UserResponse

    class Config:
        orm_mode = True