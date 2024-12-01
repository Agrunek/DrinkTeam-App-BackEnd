import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from typing import List

from app.models.instruction_step import InstructionStep
from app.models.step import Step
from app.schemas.steps_schema import StepRequestResponse

class InstructionService:

    @staticmethod
    def get_recipe_instruction(_recipe_id : int, _db : _orm.Session):

        stmt = _sql.select(InstructionStep).where(InstructionStep.recipe_id == _recipe_id).join(InstructionStep.step).order_by(_sql.asc(Step.step_number))
        
        return _db.execute(stmt).scalars().all()
    
    @staticmethod
    def add_recipe_instruction(_recipe_id : int, _recipe_instructions : List[StepRequestResponse] , _db : _orm.Session):
        #print(f"RECIPE ID = {_recipe_id}")

        check_recipe_instructions = InstructionService.get_recipe_instruction(_recipe_id,_db)

        if len(check_recipe_instructions) != 0:
            raise Exception
        
        total_preparation_time = 0

        for recipe_step in _recipe_instructions:
            #print(recipe_step)

            _new_step = Step(
                name = recipe_step.name,
                description = recipe_step.description,
                step_number = recipe_step.step_number,
                duration = recipe_step.duration
            )

            total_preparation_time += recipe_step.duration

            _new_recipe_step = InstructionStep(
                recipe_id = _recipe_id,
                step = _new_step
            )

            #print(f"STEP -> {_new_recipe_step}")
            
            _db.add( _new_recipe_step)
            _db.commit()
            _db.refresh( _new_recipe_step)

        from app.services.recipe_service import RecipeService
        # Update Recipe preparation_time field
        recipe = RecipeService.get_recipe_by_id(_recipe_id = _recipe_id, _db = _db)
        recipe.preparation_time = total_preparation_time

        _db.commit()
