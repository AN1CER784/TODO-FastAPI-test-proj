
from fastapi import APIRouter, status, Depends
from typing import List
from src.models import Task
from src.schemas import TaskScheme, TaskRead
from src.api.dependecies.db import get_task_or_404

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task_in: TaskScheme):
    task = await Task.create(**task_in.model_dump(exclude_none=True))
    return await TaskRead.from_tortoise_orm(task)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(task: Task = Depends(get_task_or_404)):
    return await TaskRead.from_tortoise_orm(task)


@router.get("/", response_model=List[TaskRead])
async def list_tasks(skip: int = 0, limit: int = 100):
    return await TaskRead.from_queryset(Task.all().offset(skip).limit(limit))


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(task_in: TaskScheme, task: Task = Depends(get_task_or_404)):
    update_data = task_in.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(task, k, v)
    await task.save()
    return await TaskRead.from_tortoise_orm(task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task: Task = Depends(get_task_or_404)):
    await task.delete()
    return None
