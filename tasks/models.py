from django.db import models, transaction
from enumchoicefield import ChoiceEnum, EnumChoiceField
from users.models import Role, User


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

    @classmethod
    @transaction.atomic
    def create_task(cls, title, assignee, created_by, priority, status, description):
        if title == "":
            raise ValueError("Title must contain at lease one character")
        assigner_role = created_by.role
        assigner_team = created_by.team
        assigne_team = assignee.team
        if assigne_team != assigner_team:
            raise ValueError("Manager can assign tasks only for his own employees")
        if assigner_role != Role.MANAGER:
            raise ValueError("User must be a manager to assign tasks")
        task = Task.objects.create(title=title,
                                   assignee=assignee,
                                   created_by=created_by,
                                   priority=priority,
                                   status=status,
                                   description=description)
        return task


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
