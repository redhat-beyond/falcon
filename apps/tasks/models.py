from django.db import models
# from tasks.models import Users
from enumchoicefield import ChoiceEnum, EnumChoiceField
import uuid


class Status(ChoiceEnum):
    BACKLOG = 'Backlog',
    IN_PROGRESS = 'InProgress',
    DONE = 'Done',


class Priority(ChoiceEnum):
    LOW = 'Low',
    MEDIUM = 'Medium',
    HIGH = 'High',
    CRITICAL = 'Critical',


class Task(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User)
    # assignee = models.ForeignKey(User)
    priority = EnumChoiceField(Priority, default=Priority.LOW, max_length=1)
    status = EnumChoiceField(Status, default=Status.BACKLOG, max_length=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    # user_id = models.ForeignKey(Users)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.id
