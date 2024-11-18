import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from typing import List

from app.models.recipe_ingredients import RecipeIngredient
from app.schemas.recipe_ingredients_schema import RecipeIngredientRequestAdd
from app.models.recipe_ingredients import RecipeIngredient

class RecipeIngredientService:

    @staticmethod
    def get_recipe_ingredients(_recipe_id : int, _db : _orm.Session):

        stmt = _sql.select(RecipeIngredient).where(RecipeIngredient.recipe_id == _recipe_id)
        
        return _db.execute(stmt).scalars().all()
    
    @staticmethod
    def add_recipe_ingredients(_recipe_ingredients : List[RecipeIngredientRequestAdd] , _db : _orm.Session):

        for recipe_ingredient in _recipe_ingredients:
            #print(recipe_ingredient)

            _new_recipe_ingredient = RecipeIngredient(
                quantity = recipe_ingredient.quantity,
                unit = recipe_ingredient.unit,
                recipe_id = recipe_ingredient.recipe_id,
                ingredient_id = recipe_ingredient.ingredient_id
            )
            
            _db.add(_new_recipe_ingredient)
            _db.commit()
            _db.refresh(_new_recipe_ingredient)

