from sqlalchemy import Integer, String, Time, DateTime, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from app.models import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    recipe_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True)

    name : Mapped[String] = mapped_column(String(50))
    image_url : Mapped[String] = mapped_column(String(100), nullable = True)
    preparation_time : Mapped[Integer] = mapped_column(Integer)
    creation_time : Mapped[DateTime] = mapped_column(DateTime)
    last_modified : Mapped[DateTime] = mapped_column(DateTime)

    description : Mapped[String] = mapped_column(String(200), nullable = False)
    alcohol_content : Mapped[Float] = mapped_column(Float, nullable = False)
    average_rating : Mapped[Float] = mapped_column(Float, nullable = False)
    number_of_reviews : Mapped[Integer] = mapped_column(Integer, nullable = False)
    difficulty : Mapped[Integer] = mapped_column(Integer, nullable = False)

    # relationship with Category
    category_id : Mapped[Integer] = mapped_column(Integer, ForeignKey('categories.category_id'))
    category : Mapped[List["Category"]] = relationship(back_populates = 'recipe')
    
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
    ingredients : Mapped[List["RecipeIngredient"]] = relationship(back_populates = 'recipe', cascade="all, delete")

    def __str__(self) -> str:
        return f"Recipe(id={self.category_id},name={self.name},image_url={self.image_url},preparation_time={self.preparation_time},creation_time={self.creation_time},last_modified={self.last_modified},category_id={self.category_id},recipe_detail_id={self.recipe_detail_id},user_id={self.user_id},)"