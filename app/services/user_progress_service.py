import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from fastapi import HTTPException
import datetime

from app.models.user_progress import UserProgress
from app.services.instruction_service import InstructionService
from app.models.instruction_step import InstructionStep
from app.models.step import Step

class UserProgressService:

    @staticmethod
    def initialize_user_progress_for_recipe(_recipe_id : int, _user_id : int, _db : _orm.Session):
        
        check_user_progress = UserProgressService.get_user_progress_for_recipe(_recipe_id, _user_id, _db)

        #print(check_user_progress)

        if len(check_user_progress) != 0:
            raise HTTPException(status_code=404, detail = f"User id = {_user_id} already started this recipe id = {_recipe_id} !")

        instruction_steps = InstructionService.get_recipe_instruction(_recipe_id = _recipe_id, _db = _db)

        #print(instruction_steps)

        for step in instruction_steps:

            new_user_progress = UserProgress(
                started_date = None,
                finished_date = None,
                completed = False,
                recipe_id = _recipe_id,
                user_id = _user_id,
                instruction_step = step
            )

            _db.add(new_user_progress)
            _db.commit()
            _db.refresh(new_user_progress)

    
    @staticmethod
    def get_user_progress_for_recipe(_recipe_id : int, _user_id : int, _db : _orm.Session):
        
        stmt = (
            _sql.select(UserProgress)
            .join(UserProgress.instruction_step)
            .join(InstructionStep.step)
            .where(
                UserProgress.recipe_id == _recipe_id,
                UserProgress.user_id == _user_id
            )
            .order_by(_sql.asc(Step.step_number))
        )

        return _db.execute(stmt).scalars().all()
    

    @staticmethod
    def update_user_progress():
        pass