import sqlalchemy as _sql
from sqlalchemy.orm import sessionmaker
import json
from app.models import Base

from app.models.category import Category
from app.models.ingredient import Ingredient
from app.models.recipe_ingredients import RecipeIngredient
from app.models.user import User
from app.models.user_progress import UserProgress
from app.models.review import Review
from app.models.category import Category
from app.models.recipe import Recipe
from app.models.step import Step
from app.models.instruction_step import InstructionStep

password = None

with open("./app/password.json", "r") as file:
    password = json.load(file)
    password = password['DRINK_TEAM_DATABASE_PASSWORD']


connection_string = f"mssql+pyodbc://admin_database:{password}@drink-team.database.windows.net:1433/drink_team_db?driver=ODBC+Driver+17+for+SQL+Server" # CONNECT TO AZURE SQL DATABASE
#connection_string = f"mysql+mysqlconnector://root:password123@127.0.0.1:3306/drink-team" # CONNECT TO MYSQL DOCKER
#connection_string = f"mysql+mysqlconnector://root:password123@mysql:3306/drink-team" # CONNECT TO DOCKER MYSQL VIA FAST API DOCKER
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

