import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from datetime import datetime

from MainDirectory.models.recipe import Recipe
from MainDirectory.models.recipe_details import RecipeDetail
from MainDirectory.schemas.recipe_schema import RecipeRequestAdd

class RecipeService:

    @staticmethod
    def get_all_recipes(_sort_rating : str, _sort_prep_time : str, _db : _orm.Session):
        
        rating_order = _sql.asc(RecipeDetail.total_rating) if _sort_rating == "asc" else _sql.desc(RecipeDetail.total_rating)
        prep_time_order = _sql.asc(Recipe.preparation_time) if _sort_prep_time == "asc" else _sql.desc(Recipe.preparation_time)

        stmt = _sql.select(Recipe).join(Recipe.recipe_detail).order_by(rating_order,prep_time_order)

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
        
        new_recipe_detail = RecipeDetail(
            description = _new_recipe.recipe_detail.description,
            type = _new_recipe.recipe_detail.type,
            alcohol_content = _new_recipe.recipe_detail.alcohol_content,
            total_rating = _new_recipe.recipe_detail.total_rating,
            difficulty = _new_recipe.recipe_detail.difficulty
        )

        new_recipe = Recipe(
            name = _new_recipe.name,
            image_url = _new_recipe.image_url,
            preparation_time = _new_recipe.preparation_time,
            creation_time = datetime.now(),
            last_modified = datetime.now(),
            category_id = _new_recipe.category_id,
            recipe_detail = new_recipe_detail,
            user_id = _new_recipe.user_id,
        )

        _db.add(new_recipe)
        _db.commit()
        _db.refresh(new_recipe)
        

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
            recipe.preparation_time = _updated_recipe.preparation_time
            recipe.last_modified = datetime.now()
            recipe.recipe_detail.description = _updated_recipe.recipe_detail.description
            recipe.recipe_detail.type = _updated_recipe.recipe_detail.type
            recipe.recipe_detail.alcohol_content = _updated_recipe.recipe_detail.alcohol_content
            recipe.recipe_detail.total_rating = _updated_recipe.recipe_detail.total_rating
            recipe.recipe_detail.difficulty = _updated_recipe.recipe_detail.difficulty
            _db.commit()
        except Exception as e:
            print("ERROR ", e)
            raise Exception