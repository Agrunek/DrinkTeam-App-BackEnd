from pydantic import BaseModel

class CategoryRequest(BaseModel):
    name : str
    description : str

    model_config = {
        "from_attributes": True
    }

class CategoryResponse(BaseModel):
    category_id : int
    name : str
    description : str

    model_config = {
        "from_attributes": True
    }