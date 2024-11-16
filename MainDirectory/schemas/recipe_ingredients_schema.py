from pydantic import BaseModel

from MainDirectory.schemas.ingredient_schema import IngredientResponse

class RecipeIngredientRequestAdd(BaseModel):
    recipe_id : int
    ingredient_id : int
    quantity : float
    unit : str

    class Config:
        orm_mode = True


class RecipeIngredientResponse(BaseModel):
    recipe_id : int
    ingredient : IngredientResponse
    quantity : float
    unit : str

    class Config:
        orm_mode = True