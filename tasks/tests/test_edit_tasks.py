from tasks.models import Status, Priority, Task
import pytest


@pytest.mark.django_db
class TestEditTasks:

    def test_update_status(self, task_1):
        assert task_1.status == Status.IN_PROGRESS
        task_1.update_status(Status.DONE)
        assert task_1.status == Status.DONE
        assert Task.objects.get(pk=task_1.id).status == Status.DONE

    def test_update_priority(self, task_1):
        assert task_1.priority == Priority.HIGH
        task_1.update_priority(Priority.LOW)
        assert task_1.priority == Priority.LOW
        assert Task.objects.get(pk=task_1.id).priority == Priority.LOW
