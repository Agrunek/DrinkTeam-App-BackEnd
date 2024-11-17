import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from MainDirectory.models.category import Category
from MainDirectory.schemas.category_schema import CategoryRequest

class CategoryService:

    @staticmethod
    def add_category(_category_request : CategoryRequest, _db : _orm.Session):
        new_Category = Category(
            name = _category_request.name,
            description = _category_request.description
        )
        _db.add(new_Category)
        _db.commit()
        _db.refresh(new_Category)

    @staticmethod
    def get_all_categories(_db : _orm.Session):
        stmt = _sql.select(Category)
        return _db.execute(stmt).all()

    @staticmethod
    def get_category_by_id(_category_id : int, _db : _orm.Session):
        stmt = _sql.select(Category).where(Category.category_id == _category_id)
        return _db.execute(stmt).first()[0]

    @staticmethod
    def update_category(_db : _orm.Session):
        pass

