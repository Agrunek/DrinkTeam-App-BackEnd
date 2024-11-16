from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
import fastapi as _fastapi
from typing import List

from MainDirectory.database.database import get_session

from MainDirectory.services.recipe_ingridient_service import RecipeIngredientService
from MainDirectory.schemas.recipe_ingredients_schema import RecipeIngredientResponse

recipe_ingredient_router = APIRouter(
    prefix="/recipe_ingredients",
    tags=["recipe_ingredients"]
)

@recipe_ingredient_router.get("/test")
def test():
    return {"test": "test"}

@recipe_ingredient_router.get("/{recipe_id}", response_model = List[RecipeIngredientResponse], status_code = status.HTTP_200_OK)
def get_recipe_ingredients(recipe_id : int, db : _orm.Session = Depends(get_session)):
    recipe_ingredients = RecipeIngredientService.get_recipe_ingredients(_recipe_id = recipe_id, _db = db)

    if not recipe_ingredients:
        raise HTTPException(status_code = 404, detail = f"No recipes ingredients id = {recipe_id} found !")
    
    return recipe_ingredients

