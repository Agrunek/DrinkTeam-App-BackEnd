from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
from typing import List

from app.services.recipe_service import RecipeService
from app.services.recipe_ingridient_service import RecipeIngredientService
from app.services.instruction_service import InstructionService
from app.database.database import get_session
from app.schemas.recipe_schema import RecipeResponse, RecipeRequestAdd, RecipeIngredientsStepsResponse, RecipeIngredientsStepsRequest

recipe_router = APIRouter(
    prefix="/recipe",
    tags=["recipes"]
)

@recipe_router.get("/test")
def test():
    return {"test": "test"}

@recipe_router.get("/all", response_model = List[RecipeResponse], status_code = status.HTTP_200_OK)
def get_all_recipes(sort_rating : str | None = None,
                    sort_prep_time : str | None = None,
                    sort_difficulty : str | None = None,
                    db : _orm.Session = Depends(get_session)):

        recipes = RecipeService.get_all_recipes(_sort_rating = sort_rating,
                                                _sort_prep_time = sort_prep_time,
                                                _sort_difficulty = sort_difficulty,
                                                _db = db)

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
        

@recipe_router.get("/{recipe_id}/recipe_extra", response_model = RecipeIngredientsStepsResponse, status_code = status.HTTP_200_OK)
def get_recipe_ingredients_and_steps(recipe_id : int, db : _orm.Session = Depends(get_session)):

    recipe_check = RecipeService.get_recipe_by_id(_recipe_id = recipe_id, _db = db)

    if not recipe_check:
        raise HTTPException(status_code=404, detail = f"Can not find recipe id = {recipe_id}!")

    recipe_ingredients = RecipeIngredientService.get_recipe_ingredients(_recipe_id = recipe_id, _db = db)
    recipe_instructions = InstructionService.get_recipe_instruction(_recipe_id = recipe_id, _db = db)
    #print(recipe_instructions)

    recipe_ingredients_instruction = RecipeIngredientsStepsResponse(
        ingredients = recipe_ingredients,
        steps = recipe_instructions
    )

    return recipe_ingredients_instruction


@recipe_router.post("/recipe_extra/add", status_code = status.HTTP_201_CREATED)
def add_recipe_ingredients_and_instruction(recipe_ingredients_instruction : RecipeIngredientsStepsRequest, db : _orm.Session = Depends(get_session)):
    
    try: 
        RecipeService.add_recipe_ingredients_and_instruction(_recipe_ingredients_instruction = recipe_ingredients_instruction, _db = db)

        return {"SUCCESS" : f"New Recipe Ingredients and Instruction for recipe id = {recipe_ingredients_instruction.recipe_id} was added successfully !"}
    
    except TypeError:
        raise HTTPException(status_code=404, detail = f"Can not add because recipe not exist !")
    except Exception as e:
        print("EXCEPTION: ", e)
        db.rollback()
        raise HTTPException(status_code=404, detail = f"Can not add new recipe ingredients and instruction !")
    