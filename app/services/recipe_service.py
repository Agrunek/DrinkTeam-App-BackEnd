import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from datetime import datetime
from fastapi import UploadFile

from app.models.recipe import Recipe
from app.schemas.recipe_schema import RecipeRequestAdd, RecipeIngredientsStepsRequest
from app.services.recipe_ingridient_service import RecipeIngredientService
from app.services.instruction_service import InstructionService

class RecipeService:

    @staticmethod
    def get_all_recipes(_sort_rating : str | None, _sort_prep_time : str | None, _sort_difficulty : str | None, _db : _orm.Session):
        
        rating_order = None if _sort_rating == None else _sql.asc(Recipe.average_rating) if _sort_rating == "asc" else _sql.desc(Recipe.average_rating)
        prep_time_order = None if _sort_prep_time == None else _sql.asc(Recipe.preparation_time) if _sort_prep_time == "asc" else _sql.desc(Recipe.preparation_time)
        difficulty_order = None if _sort_difficulty == None else _sql.asc(Recipe.difficulty) if _sort_difficulty == "asc" else _sql.desc(Recipe.difficulty)

        print(f"Check: {rating_order} | {prep_time_order} | {difficulty_order}")

        order_criteria = []
        if rating_order is not None:
            order_criteria.append(rating_order)
        if prep_time_order is not None:
            order_criteria.append(prep_time_order)
        if difficulty_order is not None:
            order_criteria.append(difficulty_order)

        print(order_criteria)

        stmt = _sql.select(Recipe).order_by(*order_criteria)

        return _db.execute(stmt).scalars().all()
    

    @staticmethod
    def get_recipe_by_id(_recipe_id : int, _db : _orm.Session):
        stmt = _sql.select(Recipe).where(Recipe.recipe_id == _recipe_id)
        res = _db.execute(stmt).scalars().first()
        return None if res is None else res
    

    @staticmethod
    def get_recipes_by_category_id(_category_id : int, _db : _orm.Session):
        stmt = _sql.select(Recipe).where(Recipe.category_id == _category_id)
        return _db.execute(stmt).scalars().all()
    
    
    @staticmethod
    def add_recipe(_new_recipe : RecipeRequestAdd, _db : _orm.Session):

        new_recipe = Recipe(
            name = _new_recipe.name,
            image_url = "",
            preparation_time = 0,
            creation_time = datetime.now(),
            last_modified = datetime.now(),
            description = _new_recipe.description,
            alcohol_content = _new_recipe.alcohol_content,
            average_rating = 0,
            number_of_reviews = 0,
            difficulty = _new_recipe.difficulty,
            category_id = _new_recipe.category_id,
            user_id = _new_recipe.user_id,
        )

        _db.add(new_recipe)
        _db.commit()
        _db.refresh(new_recipe)
        

    @staticmethod
    def update_image_filename(recipe_id : int,file_url : str, _db : _orm.Session):
        
        recipe = RecipeService.get_recipe_by_id(_recipe_id = recipe_id, _db = _db)
        recipe.image_url = file_url
        _db.commit()


    @staticmethod
    def delete_recipe_by_id(_recipe_id : int, _db : _orm.Session):
        
        recipe = RecipeService.get_recipe_by_id(_recipe_id, _db = _db)

        if recipe is None:
            raise Exception

        _db.delete(recipe)
        _db.commit()


    @staticmethod
    def update_recipe(_updated_recipe : RecipeRequestAdd, _db : _orm.Session):
        try:
            recipe = RecipeService.get_recipe_by_id(_recipe_id = _updated_recipe.recipe_id, _db = _db)
            print("Recipe found !!")
            if recipe is None:
                print("Recipe not found !!")
                raise Exception

            recipe.name = _updated_recipe.name
            recipe.image_url = _updated_recipe.image_url
            recipe.last_modified = datetime.now()
            recipe.description = _updated_recipe.description
            recipe.alcohol_content = _updated_recipe.alcohol_content
            recipe.difficulty = _updated_recipe.difficulty
            recipe.category_id = _updated_recipe.category_id

            _db.commit()

        except Exception as e:
            print("ERROR ", e)
            raise Exception
        

    @staticmethod
    def add_recipe_ingredients_and_instruction(_recipe_ingredients_instruction : RecipeIngredientsStepsRequest, _db : _orm.Session):

        recipe_check = RecipeService.get_recipe_by_id(_recipe_id = _recipe_ingredients_instruction.recipe_id, _db = _db)

        if not recipe_check:
            raise TypeError

        RecipeIngredientService.add_recipe_ingredients(_recipe_id = _recipe_ingredients_instruction.recipe_id,
                                                        _recipe_ingredients = _recipe_ingredients_instruction.ingredients,
                                                        _db = _db)

        InstructionService.add_recipe_instruction(_recipe_id = _recipe_ingredients_instruction.recipe_id,
                                                _recipe_instructions = _recipe_ingredients_instruction.steps,
                                                _db = _db)
        