

import uuid
from enum import Enum

from tortoise import fields, models


class TaskStatus(str, Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Task(models.Model):
    id = fields.UUIDField(primary_key=True, default=uuid.uuid4)
    title = fields.CharField(max_length=200)
    description = fields.TextField(null=True)
    status = fields.CharEnumField(TaskStatus, max_length=32, default=TaskStatus.CREATED)

    class Meta:
        table = "tasks"