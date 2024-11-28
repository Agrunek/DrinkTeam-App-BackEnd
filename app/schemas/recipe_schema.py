from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, List
from app.schemas.category_schema import CategoryResponse
from app.schemas.user_schema import UserResponse
from app.schemas.instruction_steps_schema import InstructionStepsRequestResponse, InstructionStepsRequestResponse
from app.schemas.recipe_ingredients_schema import RecipeIngredientResponse, RecipeIngredientRequestAdd
from app.schemas.steps_schema import StepRequestResponse

class RecipeRequestAdd(BaseModel):
    recipe_id : Optional[int] = None
    name : str
    description : str
    alcohol_content : float
    difficulty : int
    category_id : int
    user_id : int


class RecipeResponse(BaseModel):
    recipe_id : int
    name : str
    image_url : Optional[str] = None
    preparation_time : int
    creation_time : datetime
    last_modified : datetime
    description : str
    alcohol_content : float
    average_rating : float
    number_of_reviews : int
    difficulty : int
    category : CategoryResponse
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