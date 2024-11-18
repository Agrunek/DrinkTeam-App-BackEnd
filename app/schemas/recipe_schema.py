from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, List
from app.schemas.category_schema import CategoryResponse
from app.schemas.recipe_detail_schema import RecipeDetailResponse, RecipeDetailRequestAdd
from app.schemas.user_schema import UserResponse
from app.schemas.instruction_steps_schema import InstructionStepsRequestResponse, InstructionStepsRequestResponse
from app.schemas.recipe_ingredients_schema import RecipeIngredientResponse, RecipeIngredientRequestAdd
from app.schemas.steps_schema import StepRequestResponse

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

    model_config = {
        "from_attributes": True
    }

class RecipeIngredientsStepsRequest(BaseModel):
    recipe_id : int
    ingredients : List[RecipeIngredientRequestAdd]
    steps : List[StepRequestResponse]


class RecipeIngredientsStepsResponse(BaseModel):
    ingredients : List[RecipeIngredientResponse]
    steps : List[InstructionStepsRequestResponse]