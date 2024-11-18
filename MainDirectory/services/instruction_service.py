import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from typing import List

from MainDirectory.models.instruction_step import InstructionStep
from MainDirectory.models.step import Step
from MainDirectory.schemas.steps_schema import StepRequestResponse

class InstructionService:

    @staticmethod
    def get_recipe_instruction(_recipe_id : int, _db : _orm.Session):

        stmt = _sql.select(InstructionStep).where(InstructionStep.recipe_id == _recipe_id)
        
        return _db.execute(stmt).scalars().all()
    
    @staticmethod
    def add_recipe_instruction(_recipe_id : int, _recipe_instructions : List[StepRequestResponse] , _db : _orm.Session):
        #print(f"RECIPE ID = {_recipe_id}")

        for recipe_step in _recipe_instructions:
            #print(recipe_step)

            _new_step = Step(
                name = recipe_step.name,
                description = recipe_step.description,
                step_number = recipe_step.step_number,
                wait_time = recipe_step.wait_time
            )

            _new_recipe_step = InstructionStep(
                recipe_id = _recipe_id,
                step = _new_step
            )

            #print(f"STEP -> {_new_recipe_step}")
            
            _db.add( _new_recipe_step)
            _db.commit()
            _db.refresh( _new_recipe_step)
