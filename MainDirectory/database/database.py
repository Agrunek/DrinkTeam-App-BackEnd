import sqlalchemy as _sql
from sqlalchemy.orm import sessionmaker
import os
from MainDirectory.models import Base

from MainDirectory.models.category import Category
from MainDirectory.models.ingredient import Ingredient
from MainDirectory.models.recipe_ingredients import RecipeIngredient
from MainDirectory.models.user import User
from MainDirectory.models.user_progress import UserProgress
from MainDirectory.models.review import Review
from MainDirectory.models.category import Category
from MainDirectory.models.recipe_details import RecipeDetail
from MainDirectory.models.recipe import Recipe
from MainDirectory.models.step import Step
from MainDirectory.models.instruction_step import InstructionStep

server = 'drink-team.database.windows.net:1433'
database = 'drink_team_db'
username='admin_database',
password=os.getenv("DRINK_TEAM_DATABASE_PASSWORD")
connection_string = f"mssql+pyodbc://{username[0]}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
SessionLocal = None


database_engine = _sql.create_engine(url = connection_string, echo = False)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = database_engine)

# Create connection with database
def create_database():
    Base.metadata.create_all(bind = database_engine)

# Get active session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_session_with():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

