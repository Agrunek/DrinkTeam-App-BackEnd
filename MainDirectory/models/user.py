from sqlalchemy import Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from MainDirectory.models import Base

class User(Base):
    __tablename__ = 'users'

    user_id : Mapped[int] = mapped_column(Integer, primary_key = True, index = True)
    username : Mapped[String] = mapped_column(String(30))
    email : Mapped[Integer] = mapped_column(String(50))
    password : Mapped[String] = mapped_column(String(60))
    date_of_birth : Mapped[DateTime] = mapped_column(DateTime)
    creation_date : Mapped[DateTime] = mapped_column(DateTime)

    # # relationship with Recipe
    recipe : Mapped["Recipe"] = relationship(back_populates='user')

    # # relationship with Review
    review : Mapped["Review"] = relationship(back_populates = 'users')

    # relationship with UserProgress
    recipes: Mapped[List["UserProgress"]] = relationship(back_populates='user')
