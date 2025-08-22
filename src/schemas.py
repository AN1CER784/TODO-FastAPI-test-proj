from typing import Optional, Literal

from pydantic import Field
from tortoise.contrib.pydantic import PydanticModel
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Task


class TaskScheme(PydanticModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[Literal['created', 'in_progress', 'completed']] = None


TaskRead = pydantic_model_creator(Task, name="TaskRead")
