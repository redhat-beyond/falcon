import pytest
from tasks.models import Task


@pytest.mark.django_db
class TestChangeTaskAssignee:
    def test_change_task_assignee(self, test_db):
        _, employees, _, _ = test_db
        task = Task.objects.filter(assignee=employees[0]).first()
        assert task is not None
        task.change_assignee(employees[1])
        assert task.assignee == employees[1]
