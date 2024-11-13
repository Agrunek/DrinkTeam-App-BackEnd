from pydantic import BaseModel

class CategoryRequest(BaseModel):
    name : str
    description : str

class CategoryResponse(BaseModel):
    category_id : int
    name : str
    description : str

    class Config:
        orm_mode = True