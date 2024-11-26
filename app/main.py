import fastapi
from fastapi.middleware.cors import CORSMiddleware

from app.routers.recipe_router import recipe_router
from app.routers.user_router import user_router
from app.routers.recipe_ingredients_router import recipe_ingredient_router
from app.routers.review_router import review_router

from app.database.database import create_database

create_database()

app = fastapi.FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recipe_router)
app.include_router(user_router)
app.include_router(recipe_ingredient_router)
app.include_router(review_router)

@app.get("/test")
async def test():
    return {
        "Connection status: " : "CONNECTED"
    }
