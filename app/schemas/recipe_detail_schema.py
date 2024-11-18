from pydantic import BaseModel

class RecipeDetailRequestAdd(BaseModel):
    description : str
    type : str
    alcohol_content : float
    total_rating : float
    difficulty : int

    model_config = {
        "from_attributes": True
    }

class RecipeDetailResponse(BaseModel):
    recipe_detail_id : int
    description : str
    type : str
    alcohol_content : float
    total_rating : float
    difficulty : int

    model_config = {
        "from_attributes": True
    }