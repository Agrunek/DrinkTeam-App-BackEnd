from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models import Base

class Review(Base):
    __tablename__ = 'reviews'

    review_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    comment : Mapped[String] = mapped_column(String)
    rating : Mapped[Integer] = mapped_column(Integer, nullable = False)
    creation_date : Mapped[DateTime] = mapped_column(DateTime)

    # relationship with Recipe
    recipe_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('recipes.recipe_id'))
    recipes : Mapped[List["Recipe"]] = relationship(back_populates='review')

    # relationship with User
    user_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('users.user_id'))
    users : Mapped[List["User"]] = relationship(back_populates='review')

