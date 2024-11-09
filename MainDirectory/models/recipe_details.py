from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base

from models.recipe import Recipe


class RecipeDetail(Base):
    __tablename__ = 'recipe_details'

    recipe_detail_id : Mapped[int] = mapped_column(Integer, primary_key = True, nullable = False, index = True)
    description : Mapped[String] = mapped_column(String(100), nullable = False)
    type : Mapped[String] = mapped_column(String(30), nullable = False)
    alcohol_content : Mapped[Float] = mapped_column(Float, nullable = False)
    total_rating : Mapped[Float] = mapped_column(Float, nullable = False)
    difficulty : Mapped[Integer] = mapped_column(Integer, nullable = False)

    #relationship with Recipe
    recipe : Mapped["Recipe"] = relationship("Recipe", back_populates='recipe_detail')