from fastapi import HTTPException, status
from src.models import Task
from typing import Union
from uuid import UUID


async def get_task_or_404(task_id: Union[str, UUID]) -> Task:
    task = await Task.get_or_none(id=task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task
