import sqlalchemy as _sql
import sqlalchemy.orm as _orm
from datetime import datetime

from app.models.review import Review
from app.schemas.review_schema import ReviewRequestAdd

class ReviewService:

    @staticmethod
    def get_all_reviews_for_recipe(_recipe_id : int, _db : _orm.Session):
        stmt = _sql.select(Review).where(Review.recipe_id == _recipe_id).order_by(_sql.desc(Review.creation_date))

        return _db.execute(stmt).scalars().all()

    @staticmethod
    def add_new_review(_new_review : ReviewRequestAdd, _db : _orm.Session):
        
        new_review = Review(
            comment = _new_review.comment,
            rating = _new_review.rating,
            creation_date = datetime.now(),
            recipe_id = _new_review.recipe_id,
            user_id = _new_review.user_id
        )

        _db.add(new_review)
        _db.commit()
        _db.refresh(new_review)
