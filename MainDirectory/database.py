import sqlalchemy as _sql
from sqlalchemy.orm import sessionmaker
import os
from models.recipe import Recipe, Base

class DatabaseHandler:
    server = 'drink-team.database.windows.net:1433'
    database = 'drink_team_db'
    username='admin_database',
    password=os.getenv("DRINK_TEAM_DATABASE_PASSWORD")
    connection_string = f"mssql+pyodbc://{username[0]}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

    # Create connection with database
    def __init__(self) -> None:
        self.database_engine = _sql.create_engine(url = self.connection_string, echo = False)
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
    result = session.execute(_sql.text("SELECT * FROM Table_1"))

    for x in result:
        print(x)

    # new_recipe = Recipe(name="test1234543")

    # session.add(new_recipe)
    # session.commit()
    # session.refresh(new_recipe)

    result = session.query(Recipe).all()

    for recipe in result:
        print(f"ID: {recipe.id}, Name: {recipe.name}")
