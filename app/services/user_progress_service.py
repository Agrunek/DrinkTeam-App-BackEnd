import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from fastapi import HTTPException
from datetime import datetime

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

        for idx, step in enumerate(instruction_steps):

            new_user_progress = UserProgress(
                started_date = None,
                finished_date = None,
                completed = False,
                recipe_id = _recipe_id,
                user_id = _user_id,
                instruction_step = step
            )

            if idx == 0:
                new_user_progress.started_date = datetime.now()

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
    def update_user_progress(_user_id : int, _recipe_id : int, _go_next_step : bool, _db : _orm.Session):

        user_progress = UserProgressService.get_user_progress_for_recipe(_recipe_id = _recipe_id, _user_id = _user_id, _db = _db)

        index_last_completed_step = None

        for idx, step in enumerate(user_progress):
            
            if not step.completed:
                index_last_completed_step = idx
                break

        # Finish previous step and go to next
        if _go_next_step:

            #print(f"Index of last completed step : {index_last_completed_step}")

            if index_last_completed_step == None:
                raise HTTPException(status_code= 404, detail = f"User id = {_user_id} already completed progress for recipe id = {_recipe_id}")

            # Update user progress
            current_user_progress = user_progress[index_last_completed_step]

            #print(f"user progress id ->  {current_user_progress.user_progress_id}")

            current_user_progress.completed = True
            current_user_progress.finished_date = datetime.now()

            if index_last_completed_step + 1 < len(user_progress):
                next_user_progress = user_progress[index_last_completed_step + 1]
                next_user_progress.started_date = datetime.now()

            _db.commit()

        # Back to previous step
        else:
            
            if index_last_completed_step == 0:
                raise HTTPException(status_code= 404, detail = f"User progress for recipe id = {_recipe_id} is on first step !!")

            print(f"index last {index_last_completed_step}")

            # if end is reached
            if index_last_completed_step == None:
                index_last_completed_step = len(user_progress) - 1

            current_user_progress = user_progress[index_last_completed_step]

            current_user_progress.completed = False
            current_user_progress.started_date = None

            if index_last_completed_step == len(user_progress) - 1:
                user_progress[index_last_completed_step].finished_date = None


            if index_last_completed_step - 1 >= 0:
                previous_user_progress = user_progress[index_last_completed_step - 1]
                previous_user_progress.finished_date = None
                previous_user_progress.completed = False

            _db.commit()


