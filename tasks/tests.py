from tasks.models import Status, Priority, Task, Comment

def test_update_status(status_1):
    assert isinstance(status_1, Task)


def test_update_priority(priority_1):
    assert isinstance(priority_1, Task)
