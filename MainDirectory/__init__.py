import azure.functions as func

import fastapi

app = fastapi.FastAPI()

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