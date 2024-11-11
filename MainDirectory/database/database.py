import sqlalchemy as _sql
from sqlalchemy.orm import sessionmaker
import os
from MainDirectory.models import Base

class DatabaseHandler:
    server = 'drink-team.database.windows.net:1433'
    database = 'drink_team_db'
    username='admin_database',
    password=os.getenv("DRINK_TEAM_DATABASE_PASSWORD")
    connection_string = f"mssql+pyodbc://{username[0]}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
    SessionLocal = None

    # Create connection with database
    @staticmethod
    def create_database(self) -> None:
        self.database_engine = _sql.create_engine(url = self.connection_string, echo = True)
        self.SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = self.database_engine)
        Base.metadata.create_all(bind = self.database_engine)

    @staticmethod
    # Get active session
    def get_session(self):
        try:
            session = self.SessionLocal()
            return session
        finally:
            session.close()

def get_session():
    db = DatabaseHandler.SessionLocal()
    try:
        yield db
    finally:
        db.close()

