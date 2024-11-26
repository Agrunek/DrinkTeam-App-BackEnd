from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
import fastapi as _fastapi
from typing import List

from app.database.database import get_session
from app.schemas.review_schema import ReviewResponse, ReviewRequestAdd
from app.services.review_service import ReviewService

review_router = APIRouter(
    prefix="/review",
    tags=["reviews"]
)

@review_router.get("/test")
def test():
    return {"test": "test"}


@review_router.get("/all/{recipe_id}", response_model = List[ReviewResponse], status_code = status.HTTP_200_OK)
def get_all_reviews_for_recipe(recipe_id : int, db : _orm.Session = Depends(get_session)):

    reviews = ReviewService.get_all_reviews_for_recipe(_recipe_id = recipe_id, _db = db)

    if not reviews:
        raise HTTPException(status_code = 404, detail = f"No reviews found for recipe id = {recipe_id} !")

    return reviews


@review_router.post("/add", status_code = status.HTTP_201_CREATED)
def add_new_review(new_review_ : ReviewRequestAdd, db : _orm.Session = Depends(get_session)):

    try: 
        ReviewService.add_new_review(_new_review = new_review_, _db = db)

        return {"SUCCESS" : f"New Review for recipe id = {new_review_.recipe_id} was added successfully !"}
        
    except Exception:
        db.rollback()
        raise HTTPException(status_code=404, detail = f"Can not add new review !")
