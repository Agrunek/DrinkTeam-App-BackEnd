from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models import Base


class InstructionStep(Base):
    __tablename__ = 'instruction_steps'

    ingredient_step_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True, autoincrement = True)

    # relationship with Ingridient - Step
    recipe_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('recipes.recipe_id'))
    step_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('steps.step_id'))

    step : Mapped[List["Step"]] = relationship(back_populates='recipes')
    recipe : Mapped["Recipe"] = relationship(back_populates='steps')
    