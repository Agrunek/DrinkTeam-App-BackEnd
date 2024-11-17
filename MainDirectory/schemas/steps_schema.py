from pydantic import BaseModel
from datetime import datetime, time
from typing import Optional, List

class StepRequestResponse(BaseModel):
    name : str
    description : str
    step_number : int
    wait_time : time

    model_config = {
        "from_attributes": True
    }