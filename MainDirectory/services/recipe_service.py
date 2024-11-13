import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from datetime import datetime

from MainDirectory.models.recipe import Recipe
from MainDirectory.schemas.recipe_schema import RecipeRequestAdd

class RecipeService:

    @staticmethod
    def get_all_recipes(_db : _orm.Session):
        stmt = _sql.select(Recipe)
        return _db.execute(stmt).scalars().all()
    
    @staticmethod
    def get_recipe_by_id(_recipe_id : int, _db : _orm.Session):
        stmt = _sql.select(Recipe).where(Recipe.recipe_id == _recipe_id)
        res = _db.execute(stmt).scalars().first()
        return None if res is None else res
    
    @staticmethod
    def add_recipe(_new_recipe : RecipeRequestAdd, _db : _orm.Session):
        
        new_recipe = Recipe(
            name = _new_recipe.name,
            image_url = _new_recipe.image_url,
            preparation_time = _new_recipe.preparation_time,
            creation_time = datetime.now(),
            last_modified = datetime.now(),
            category_id = _new_recipe.category_id,
            recipe_detail_id =_new_recipe.recipe_detail_id,
            user_id = _new_recipe.user_id,
        )

        _db.add(new_recipe)
        _db.commit()
        _db.refresh(new_recipe)
        