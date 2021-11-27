from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from users.models import User


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
    title = models.CharField(max_length=200, blank=False, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    assignee = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='assigneeTasks')
    created_by = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='createdTasks')
    priority = EnumChoiceField(Priority, default=Priority.LOW, max_length=1)
    status = EnumChoiceField(Status, default=Status.BACKLOG, max_length=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title

    @classmethod
    def filter_by_status(cls, status_filter):
        if not isinstance(status_filter, Status):
            raise ValueError
        return cls.objects.filter(status=status_filter)

    @classmethod
    def filter_by_assignee(cls, assignee_id):
        if not isinstance(assignee_id, int):
            raise TypeError
        try:
            user = User.objects.get(pk=assignee_id)
        except User.DoesNotExist:
            raise ValueError
        return cls.objects.filter(assignee=user)

    @classmethod
    def filter_by_symbol(cls, priority_filter):
        if not isinstance(priority_filter, Priority):
            raise ValueError
        print(priority_filter)
        return cls.objects.filter(priority=priority_filter)

    def update_status(self, status):
        self.status = status
        self.save()

    def update_priority(self, priority):
        self.priority = priority
        self.save()


class Comment(models.Model):
    appUser = models.ForeignKey(
        User, on_delete=models.RESTRICT, related_name='appUser')
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='task')
    title = models.CharField(max_length=200, blank=False, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title
