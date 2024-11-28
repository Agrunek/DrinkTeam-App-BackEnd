from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from app.schemas.instruction_steps_schema import InstructionStepsRequestResponse

class UserProgressResponse(BaseModel):
    user_progress_id : int

    started_date : Optional[datetime]
    finished_date : Optional[datetime]
    completed : Optional[bool]

    recipe_id : int
    user_id : int

    instruction_step : InstructionStepsRequestResponse

    model_config = {
        "from_attributes": True
    }