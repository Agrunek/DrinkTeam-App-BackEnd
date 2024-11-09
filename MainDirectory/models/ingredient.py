from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models import Base


class Ingredient(Base):
    __tablename__ = 'ingredients'

    ingredient_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    name : Mapped[String] = mapped_column(String(50))
    type : Mapped[String] = mapped_column(String(30))

    # # relationship Many-To-Many with RecipeIngridients
    recipes : Mapped[List["RecipeIngredient"]] = relationship(back_populates = 'ingredient')