import uvicorn
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from src.config import DATABASE_URL, APP_TITLE
from src.api.routers import tasks_router

app = FastAPI(title=APP_TITLE)

app.include_router(tasks_router)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["src.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
