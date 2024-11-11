from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from MainDirectory.models import Base


class RecipeIngredient(Base):
    __tablename__ = 'recipe_ingredients'

    quantity : Mapped[float] = mapped_column(Float)
    unit : Mapped[String] = mapped_column(String(30))

    # relationship with Recipe - Ingridients
    recipe_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('recipes.recipe_id'), primary_key = True)
    ingredient_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('ingredients.ingredient_id'), primary_key = True)

    ingredient : Mapped["Ingredient"] = relationship(back_populates = 'recipes')
    recipe : Mapped["Recipe"] = relationship(back_populates = 'ingredients')