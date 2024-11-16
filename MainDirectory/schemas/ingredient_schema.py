from pydantic import BaseModel


class IngredientRequestAdd(BaseModel):
    name : str
    type : str

    class Config:
        orm_mode = True


class IngredientResponse(BaseModel):
    ingredient_id : int
    name : str
    type : str

    class Config:
        orm_mode = True