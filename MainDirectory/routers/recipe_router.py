from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
import fastapi as _fastapi
from typing import List
# from sqlalchemy import text

from MainDirectory.services.recipe_service import RecipeService
from MainDirectory.database.database import get_session
from MainDirectory.schemas.recipe_schema import RecipeResponse

recipe_router = APIRouter(
    prefix="/recipe",
    tags=["recipes"]
)

@recipe_router.get("/test")
def test():
    return {"test": "test"}

@recipe_router.get("/all", response_model = List[RecipeResponse])
def get_all_recipes(db : _orm.Session = Depends(get_session)):
        
        recipes = RecipeService.get_all_recipes(_db = db)

        if not recipes:
            raise HTTPException(status_code = 404, detail = "No recipes found !")
        
        return recipes


@recipe_router.get("/{recipe_id}", response_model = RecipeResponse, status_code = status.HTTP_200_OK)
def get_recipe_by_id(recipe_id : int, db : _orm.Session = Depends(get_session)):
        
        recipe = RecipeService.get_recipe_by_id(_recipe_id = recipe_id, _db = db)

        if recipe is None:
            raise HTTPException(status_code=404, detail = f"Recipe id = {recipe_id} not found !!")

        return recipe