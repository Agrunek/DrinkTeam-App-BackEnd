from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from models import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    name : Mapped[String] = mapped_column(String(50))
    image_url : Mapped[String] = mapped_column(String(50), nullable = True)
    preparation_time : Mapped[Time] = mapped_column(Time)
    creation_time : Mapped[DateTime] = mapped_column(DateTime)
    last_modified : Mapped[DateTime] = mapped_column(DateTime)


    # relationship with Category
    category_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('categories.category_id'))
    categories : Mapped[List["Category"]] = relationship(back_populates = 'recipe')

    # # relationship with Recipe_Details
    recipe_detail_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('recipe_details.recipe_detail_id'))
    recipe_detail : Mapped["RecipeDetail"] = relationship("RecipeDetail",back_populates = 'recipe')

    # relationship with User
    user_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('users.user_id'))
    user : Mapped[List["User"]] = relationship(back_populates = 'recipe')

    # relationship Many-To-Many by UserProgress
    users: Mapped[List["UserProgress"]] = relationship(back_populates = 'recipe')

    # relationship with Review
    review : Mapped["Review"] = relationship(back_populates = 'recipes')

    # # relationship Many-To-Many by InstructionStep
    steps : Mapped[List["InstructionStep"]] = relationship(back_populates = 'recipe')

    # # relationship Many-To-Many by RecipeIngridients
    ingredients : Mapped[List["RecipeIngredient"]] = relationship(back_populates = 'recipe')

