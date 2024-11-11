from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from MainDirectory.models import Base

from MainDirectory.models.recipe import Recipe


class Category(Base):
    __tablename__ = 'categories'

    category_id : Mapped[int] = mapped_column(Integer, primary_key = True, nullable = False, index = True)
    name : Mapped[String] = mapped_column(String(50), nullable = False)
    description : Mapped[String] = mapped_column(String(100), nullable = False)

    #relationship with Recipe
    recipe : Mapped["Recipe"] = relationship(back_populates='categories')