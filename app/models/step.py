from sqlalchemy import Integer, String, ForeignKey, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models import Base

class Step(Base):
    __tablename__ = 'steps'

    step_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    name : Mapped[String] = mapped_column(String(30))
    description : Mapped[String] = mapped_column(String(80))
    step_number : Mapped[Integer] = mapped_column(Integer)
    duration : Mapped[Integer] = mapped_column(Integer)

    # # relationship Many-To-Many with InstructionStep
    recipes : Mapped[List["InstructionStep"]] = relationship(back_populates = 'step')

    def __str__(self) -> str:
        return f"Step(step_id={self.step_id},name={self.name},description={self.description},step_number={self.step_number},duration={self.duration})"