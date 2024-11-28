from fastapi import APIRouter, Depends, HTTPException, status
import sqlalchemy.orm as _orm
from typing import List

from app.database.database import get_session
from app.services.user_progress_service import UserProgressService
from app.schemas.user_progress_schema import UserProgressResponse

user_progress_router = APIRouter(
    prefix="/user_progress",
    tags=["user_progresses"]
)

@user_progress_router.get("/test")
def test():
    return {"test": "test"}


@user_progress_router.get("/{user_id}/{recipe_id}", response_model = List[UserProgressResponse], status_code = status.HTTP_200_OK)
def get_user_progress_for_recipe(user_id : int, recipe_id : int, db : _orm.Session = Depends(get_session)):

    user_progress = UserProgressService.get_user_progress_for_recipe(_recipe_id = recipe_id, _user_id = user_id, _db = db)

    if len(user_progress) == 0:
        raise HTTPException(status_code=404, detail = f"User id = {user_id} not started this recipe id = {recipe_id} !")

    return user_progress


@user_progress_router.post("/init/{user_id}/{recipe_id}", status_code = status.HTTP_202_ACCEPTED)
def initialize_user_progress_for_recipe(user_id : int, recipe_id : int, db : _orm.Session = Depends(get_session)):
    
    UserProgressService.initialize_user_progress_for_recipe(_user_id = user_id, _recipe_id = recipe_id, _db = db)

    return {"SUCCESS" : f"User id = {user_id} just started recipe id = {recipe_id}"}


@user_progress_router.put("/update/{user_id}/{recipe_id}/{go_next_step}", status_code = status.HTTP_200_OK)
def update_user_progress(user_id : int, recipe_id : int, go_next_step : bool, db : _orm.Session = Depends(get_session)):

    UserProgressService.update_user_progress(_user_id = user_id, _recipe_id = recipe_id, _go_next_step = go_next_step, _db = db)

    return {"SUCCESS" : f"Status {go_next_step} of user progress for recipe id = {recipe_id} updated by user id = {user_id}"}

