
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://./database.db")
APP_TITLE = os.getenv("APP_TITLE", "Task Manager")
