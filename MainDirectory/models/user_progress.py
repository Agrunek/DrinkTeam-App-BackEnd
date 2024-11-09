from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models import Base


class UserProgress(Base):
    __tablename__ = 'user_progresses'

    user_progress_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True, autoincrement = True)

    started_date : Mapped[DateTime] = mapped_column(DateTime)
    finished_date : Mapped[DateTime] = mapped_column(DateTime, nullable = True)
    current_step : Mapped[Integer] = mapped_column(Integer)

    # relationship with User - Recipe by UserProgress
    recipe_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('recipes.recipe_id'), primary_key = True)
    user_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('users.user_id'), primary_key = True)

    user : Mapped["User"] = relationship(back_populates = 'recipes')
    recipe : Mapped["Recipe"] = relationship(back_populates = 'users')