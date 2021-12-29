import pytest

from conftest import DEFAULT_VALID_PASSWORD
from tasks.models import Task, Priority, Status
from users.models import User


@pytest.mark.django_db
class TestAllTasksView:
    def test_not_authenticated_user_access_restricted(self, client, test_db):
        response = client.get('/tasks/')
        assert response.status_code == 200
        assert 'tasks' not in response.context.keys()

    @pytest.mark.parametrize('employee_flag', [True, False],
                             ids=[
                                 "employee",
                                 "manager"
                             ])
    def test_authenticated_user_tasks_view(self, client, test_db, employee_flag):
        users = test_db[1] if employee_flag else test_db[2]
        assert len(users) > 0
        user = users[0]
        assert isinstance(user, User)
        client.login(username=user.user.username,
                     password=DEFAULT_VALID_PASSWORD)
        response = client.get('/tasks/', enforce_csrf_checks=True)
        assert response.status_code == 200
        assert 'tasks' in response.context.keys()
        assert all(isinstance(task, Task) for task in response.context['tasks'])
        assert len(response.context['tasks']) > 0
        if employee_flag:
            assert all(task.assignee == user for task in response.context['tasks'])
        else:
            assert all(task.assignee.team == user.team for task in response.context['tasks'])

    def test_filter_task_by_priority_and_status(self, client, test_db):
        user = test_db[1][0]
        client.login(username=user.user.username, password=DEFAULT_VALID_PASSWORD)
        response = client.post('/tasks/', data={'priority': 'Low', 'status': 'Backlog'})
        assert all(task.priority == Priority.LOW and task.status == Status.BACKLOG for task in response.context['tasks']
                   )

    @pytest.mark.parametrize('user_type, priority_text, status_text',
                             [
                                 (1, 'Low', ""),
                                 (1, 'Medium', ""),
                                 (1, 'High', ""),
                                 (1, 'Critical', ""),
                                 (2, 'Low', ""),
                                 (2, 'Medium', ""),
                                 (2, 'High', ""),
                                 (2, 'Critical', "")
                             ],
                             ids=[
                                 'employee - Low',
                                 'employee - Medium',
                                 'employee - High',
                                 'employee - Critical',
                                 'manager - Low',
                                 'manager - Medium',
                                 'manager - High',
                                 'manager - Critical'
                             ]
                             )
    def test_filter_task_by_priority_not_randomized(self, client, test_db, priority_text, user_type, status_text):
        priority_dict = {
            'Low': Priority.LOW,
            'Medium': Priority.MEDIUM,
            'High': Priority.HIGH,
            'Critical': Priority.CRITICAL
        }
        user = test_db[user_type][0]
        priority = priority_dict[priority_text]
        client.login(username=user.user.username, password=DEFAULT_VALID_PASSWORD)
        response = client.post('/tasks/', data={'priority': priority_text, 'status': status_text})
        assert all(task.priority == priority for task in response.context['tasks'])

    @pytest.mark.parametrize('user_type,status_text, priority_text',
                             [
                                 (1, 'Backlog', ""),
                                 (1, 'InProgress', ""),
                                 (1, 'Done', ""),
                                 (2, 'Backlog', ""),
                                 (2, 'InProgress', ""),
                                 (2, 'Done', ""),
                             ],
                             ids=[
                                 'employee - Backlog',
                                 'employee - InProgress',
                                 'employee - High',
                                 'manager - Backlog',
                                 'manager - InProgress',
                                 'manager - Done',
                             ]
                             )
    def test_filter_task_by_status_not_randomized(self, client, test_db, status_text, user_type, priority_text):
        status_dict = {
            'Backlog': Status.BACKLOG,
            'InProgress': Status.IN_PROGRESS,
            'Done': Status.DONE,
        }
        user = test_db[user_type][0]
        status = status_dict[status_text]
        client.login(username=user.user.username, password=DEFAULT_VALID_PASSWORD)
        response = client.post('/tasks/', data={'status': status_text, 'priority': priority_text})
        assert all(task.status == status for task in response.context['tasks'])
