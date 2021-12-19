from tasks.forms import TaskForm
from tasks.models import Task
import pytest


@pytest.mark.django_db
class TestViewNewTask:

    def test_no_authenticated_create_task(self, client):
        response = client.get('/tasks/create')
        assert response.status_code == 200
        assert 'not_auth_user' in response.context.keys()

    def test_employee_create_task(self, client, employee_1):
        client.login(username=employee_1.user.username, password='password')
        response = client.get('/tasks/create')
        assert response.status_code == 200
        assert 'not_auth_user' not in response.context.keys()

    def test_manager_create_task(self, client, manager_1):
        client.login(username=manager_1.user.username, password='password')
        response = client.get('/tasks/create')
        assert response.status_code == 200
        assert 'form' in response.context.keys()

    def test_view_task_form(self, client, manager_1):
        client.login(username=manager_1.user.username, password='password')
        response = client.get('/tasks/create')
        assert response.status_code == 200
        assert isinstance(response.context.get('form'), TaskForm)

    def test_create_new_task_valid(self, client, manager_1, valid_task_data):
        i = 1
        for task in valid_task_data:
            client.login(username=manager_1.user.username, password='password')
            response = client.post('/tasks/create', data=task)
            assert response.status_code == 200
            new_task = Task.objects.get(id=i)
            assert new_task.title == task['title']
            assert new_task.assignee.user.id == task['assignee']
            assert new_task.created_by.user.id == task['created_by']
            assert new_task.priority.__str__().upper() == task['priority']
            assert new_task.status.__str__().upper() == task['status']
            assert new_task.description == task['description']
            i += 1

    def test_create_new_task_invalid(self, client, manager_1, invalid_task_data):
        client.login(username=manager_1.user.username, password='password')

        for task in invalid_task_data:
            with pytest.raises(Exception):
                client.post('/tasks/create', data=task)
                Task.objects.get(assignee=task['assignee'])

