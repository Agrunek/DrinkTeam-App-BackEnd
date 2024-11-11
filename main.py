import azure.functions as func
import fastapi

from MainDirectory.routers.recipe_router import recipe_router
from MainDirectory.routers.user_router import user_router
from MainDirectory.database.database import DatabaseHandler

app = fastapi.FastAPI()

app.include_router(recipe_router)
app.include_router(user_router)

DatabaseHandler.create_database(DatabaseHandler)

@app.get("/")
async def hello():
    return {
        "Hello" : "world !"
    }


@app.get("/sample")
async def index():
    return {
        "info": "Try /hello/Shivani for parameterized route123.",
    }


@app.get("/hello/{name}")
async def get_name(name: str):
    return {
        "name": name,
    }