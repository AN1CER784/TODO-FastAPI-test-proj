
import os

DATABASE_URL = os.getenv("DATABASE_URL")
APP_TITLE = os.getenv("APP_TITLE", "Task Manager")
TORTOISE_ORM = {
    "connections": {
        "default": DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["src.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}