from sqlalchemy import Integer, String, Time, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models import Base

class UserProgress(Base):
    __tablename__ = 'user_progresses'

    user_progress_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True, autoincrement = True)

    started_date : Mapped[DateTime] = mapped_column(DateTime, nullable = True)
    finished_date : Mapped[DateTime] = mapped_column(DateTime, nullable = True)
    completed : Mapped[Boolean] = mapped_column(Boolean)

    # relationship with User - Recipe by UserProgress
    recipe_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('recipes.recipe_id'))
    user_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('users.user_id'))
    instruction_steps_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('instruction_steps.ingredient_step_id'))

    user : Mapped["User"] = relationship(back_populates = 'recipes')
    recipe : Mapped["Recipe"] = relationship(back_populates = 'users')
    instruction_step : Mapped["InstructionStep"] = relationship(back_populates = 'user_progress')