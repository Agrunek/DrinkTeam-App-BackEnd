from pydantic import BaseModel
from datetime import datetime, time

class StepRequestResponse(BaseModel):
    step_number : int
    name : str
    description : str
    wait_time : time

    model_config = {
        "from_attributes": True
    }