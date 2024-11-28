from pydantic import BaseModel

from app.schemas.steps_schema import StepRequestResponse

class InstructionStepsRequestResponse(BaseModel):
    step : StepRequestResponse

    model_config = {
        "from_attributes": True
    }