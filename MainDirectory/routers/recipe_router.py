from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
import fastapi as _fastapi
from typing import List
# from sqlalchemy import text

from MainDirectory.services.recipe_service import RecipeService
from MainDirectory.database.database import get_session
from MainDirectory.schemas.recipe_schema import RecipeResponse, RecipeRequestAdd

recipe_router = APIRouter(
    prefix="/recipe",
    tags=["recipes"]
)

@recipe_router.get("/test")
def test():
    return {"test": "test"}

@recipe_router.get("/all", response_model = List[RecipeResponse], status_code = status.HTTP_200_OK)
def get_all_recipes(sort_rating : str | None = "desc", sort_prep_time : str | None = "desc", db : _orm.Session = Depends(get_session)):
        
        recipes = RecipeService.get_all_recipes(_sort_rating = sort_rating,_sort_prep_time = sort_prep_time,_db = db)

        if not recipes:
            raise HTTPException(status_code = 404, detail = "No recipes found !")
        
        return recipes


@recipe_router.get("/{recipe_id}", response_model = RecipeResponse, status_code = status.HTTP_200_OK)
def get_recipe_by_id(recipe_id : int, db : _orm.Session = Depends(get_session)):
        
        recipe = RecipeService.get_recipe_by_id(_recipe_id = recipe_id, _db = db)

        if recipe is None:
            raise HTTPException(status_code=404, detail = f"Recipe id = {recipe_id} not found !!")

        return recipe


@recipe_router.get("/category/{category_id}", response_model = List[RecipeResponse], status_code = status.HTTP_200_OK)
def get_recipes_by_category_id(category_id : int, db : _orm.Session = Depends(get_session)):
        
        recipes = RecipeService.get_recipes_by_category_id(_category_id = category_id, _db = db)

        if not recipes:
            raise HTTPException(status_code=404, detail = f"Can not find recipes with category_id = {category_id} !!")

        return recipes


@recipe_router.post("/add", status_code = status.HTTP_201_CREATED)
def add_new_recipe(_new_RecipeRequest : RecipeRequestAdd, db : _orm.Session = Depends(get_session)):
        try: 
            RecipeService.add_recipe(_new_recipe = _new_RecipeRequest, _db = db)

            return {"SUCCESS" : "New Recipe was added successfully !"}
        
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail = f"Can not add new recipe !")
        

@recipe_router.delete("/delete/{recipe_id}", status_code = status.HTTP_202_ACCEPTED)
def delete_recipe(recipe_id : int, db : _orm.Session = Depends(get_session)):
        try: 
            RecipeService.delete_recipe_by_id(_recipe_id = recipe_id, _db = db)

            return {"SUCCESS" : f"Recipe id = {recipe_id} successfully deleted!"}
        
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail = f"Can not delete recipe id = {recipe_id}!")


@recipe_router.put("/update", status_code = status.HTTP_202_ACCEPTED)
def update_recipe(update_recipe : RecipeRequestAdd, db : _orm.Session = Depends(get_session)):
        
        try: 
            print("Try to update recipe")
            RecipeService.update_recipe(_updated_recipe = update_recipe, _db = db)

            return {"SUCCESS" : f"Recipe name = {update_recipe.name} successfully updated!"}
        
        except Exception:
            db.rollback()
            raise HTTPException(status_code=404, detail = f"Can not update recipe = {update_recipe.name}!")