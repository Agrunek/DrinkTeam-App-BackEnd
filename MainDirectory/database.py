import sqlalchemy as _sql
from sqlalchemy.orm import sessionmaker
import os
from models import Base
from datetime import datetime
from datetime import time

from models.ingredient import Ingredient
from models.recipe_ingredients import RecipeIngredient
from models.user import User
from models.user_progress import UserProgress
from models.review import Review
from models.category import Category
from models.recipe_details import RecipeDetail
from models.recipe import Recipe
from models.step import Step
from models.instruction_step import InstructionStep


class DatabaseHandler:
    server = 'drink-team.database.windows.net:1433'
    database = 'drink_team_db'
    username='admin_database',
    password=os.getenv("DRINK_TEAM_DATABASE_PASSWORD")
    connection_string = f"mssql+pyodbc://{username[0]}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

    # Create connection with database
    def __init__(self) -> None:
        self.database_engine = _sql.create_engine(url = self.connection_string, echo = True)
        self.SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = self.database_engine)
        Base.metadata.create_all(bind = self.database_engine)

    # Get active session
    def get_session(self):
        try:
            session = self.SessionLocal()
            return session
        finally:
            session.close()



db_handler = DatabaseHandler()

with db_handler.get_session() as session:
    
    ## ADD EXAMPLE OBJECT TO DB

    # Add Category
    new_category = Category(name = "Picie", description = "do picia z kolegami")

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    # Add RecipeDetail
    new_recipe_detail = RecipeDetail(description = "pyszne picie ",
                                     type="picie",
                                     alcohol_content = 2.4,
                                     total_rating = 10,
                                     difficulty = 3)
    
    session.add(new_recipe_detail)
    session.commit()
    session.refresh(new_recipe_detail)

    # ADD User
    new_user = User(
        username="john_doe",
        email="john.doe@example.com",
        password="test",  # W praktyce hasło powinno być haszowane
        date_of_birth=datetime(1990, 1, 1),
        creation_date=datetime.now()
    )

    # Add Recipe
    new_recipe = Recipe(
        name="Mojito",
        image_url="/images/mojito.jpg",
        preparation_time=time(0, 10, 0),  # 10 minut
        creation_time=datetime.now(),
        last_modified=datetime.now()
    )

    new_recipe.categories = new_category
    new_recipe.recipe_detail = new_recipe_detail
    new_recipe.user = new_user

    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)

    # ADD User_Progress
    new_user_progress = UserProgress(
        started_date = datetime.now(),
        finished_date = datetime.now(),
        current_step = 3,
        user_id = new_user.user_id,
        recipe_id = new_recipe.recipe_id
    )

    session.add(new_user_progress)
    session.commit()
    session.refresh(new_user_progress)

    # ADD Review

    new_review = Review(
        comment="Świetny przepis! Smakowało całej rodzinie.",
        rating=5,
        creation_date=datetime.now(),  # ustawia bieżącą datę i godzinę
        recipe_id = new_recipe.recipe_id,
        user_id = new_user.user_id,
    )

    session.add(new_review)
    session.commit()
    session.refresh(new_review)


    # ADD Ingridient

    new_ingredient = Ingredient(
        name = 'jajka',
        type = 'nabial'
    )

    session.add(new_ingredient)
    session.commit()
    session.refresh(new_ingredient)


    # ADD RecipeIngridient

    new_recipe_ingredient = RecipeIngredient(
        quantity = 3,
        unit = 'kg',
        ingredient = new_ingredient,
        recipe = new_recipe
    )

    session.add(new_recipe_ingredient)
    session.commit()
    session.refresh(new_recipe_ingredient)

    # ADD Step

    new_step = Step(
        name = 'Add water',
        description = 'Add 200 ml of water',
        wait_time = time(0, 10, 0)
    )

    session.add(new_step)
    session.commit()
    session.refresh(new_step)


    # ADD RecipeStep

    new_recipe_step = InstructionStep(
        recipe = new_recipe,
        step = new_step
    )

    session.add(new_recipe_step)
    session.commit()
    session.refresh(new_recipe_step)


    # LIST ALL Recipe

    result = session.query(Recipe).all()

    for recipe in result:
        print(f"ID: {recipe.recipe_id}, Name: {recipe.name}")
