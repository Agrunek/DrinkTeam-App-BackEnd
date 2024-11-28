from pydantic import BaseModel
from datetime import datetime, time

class StepRequestResponse(BaseModel):
    name : str
    description : str
    step_number : int
    duration : int

    model_config = {
        "from_attributes": True
    }