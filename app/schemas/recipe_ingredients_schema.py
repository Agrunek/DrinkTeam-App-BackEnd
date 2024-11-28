from pydantic import BaseModel

from app.schemas.ingredient_schema import IngredientResponse, IngredientRequestAdd

class RecipeIngredientRequestAdd(BaseModel):
    ingredient : IngredientRequestAdd
    quantity : float
    unit : str

    model_config = {
        "from_attributes": True
    }


class RecipeIngredientResponse(BaseModel):
    recipe_id : int
    ingredient : IngredientResponse
    quantity : float
    unit : str

    model_config = {
        "from_attributes": True
    }