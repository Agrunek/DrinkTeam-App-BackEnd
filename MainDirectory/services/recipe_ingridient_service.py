import sqlalchemy as _sql
import sqlalchemy.orm as _orm

from MainDirectory.services.recipe_service import RecipeService
from MainDirectory.models.recipe_ingredients import RecipeIngredient

class RecipeIngredientService:

    @staticmethod
    def get_recipe_ingredients(_recipe_id : int, _db : _orm.Session):
        
        recipe_check = RecipeService.get_recipe_by_id(_recipe_id = _recipe_id, _db = _db)

        if not recipe_check:
            raise Exception

        stmt = _sql.select(RecipeIngredient).where(RecipeIngredient.recipe_id == _recipe_id)
        
        return _db.execute(stmt).scalars().all()