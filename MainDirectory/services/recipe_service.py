import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from MainDirectory.models.recipe import Recipe
from typing import List

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
        