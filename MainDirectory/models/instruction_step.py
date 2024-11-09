from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models import Base


class InstructionStep(Base):
    __tablename__ = 'instruction_steps'

    ingridient_step_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True, autoincrement = True)

    # relationship with Ingridient - Step
    recipe_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('recipes.recipe_id'), primary_key = True)
    step_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('steps.step_id'), primary_key = True)

    step : Mapped["Step"] = relationship(back_populates='recipes')
    recipe : Mapped["Recipe"] = relationship(back_populates='steps')
    