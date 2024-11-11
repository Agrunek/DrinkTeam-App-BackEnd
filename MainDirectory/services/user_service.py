import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import MainDirectory.models.category as _category

class UserService:

    @staticmethod
    def get_test():
        return {" test " : "test"}