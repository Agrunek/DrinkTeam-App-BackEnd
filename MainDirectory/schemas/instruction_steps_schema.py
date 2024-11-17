from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, List

from MainDirectory.schemas.steps_schema import StepRequestResponse

class InstructionStepsRequestResponse(BaseModel):
    step : StepRequestResponse

    model_config = {
        "from_attributes": True
    }