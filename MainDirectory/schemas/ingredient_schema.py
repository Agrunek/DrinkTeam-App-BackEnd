from pydantic import BaseModel


class IngredientRequestAdd(BaseModel):
    name : str
    type : str

    model_config = {
        "from_attributes": True
    }


class IngredientResponse(BaseModel):
    ingredient_id : int
    name : str
    type : str

    model_config = {
        "from_attributes": True
    }