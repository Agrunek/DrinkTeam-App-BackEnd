from pydantic import BaseModel

from MainDirectory.schemas.ingredient_schema import IngredientResponse, IngredientRequestAdd

class RecipeIngredientRequestAdd(BaseModel):
    recipe_id : int
    ingredient_id : int
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