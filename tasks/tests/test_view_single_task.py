from tasks.models import Status, Task
from tasks.forms import ViewTaskForm
import pytest


@pytest.mark.django_db
class TestViewSingleTask:

    def test_no_authenticated_user_asks_task(self, client, task_1):
        response = client.get(f'/tasks/{task_1.id}')
        assert response.status_code == 302
        assert response.url == '/'

    def test_with_employee_logged_in(self, client, task_1, employee_1):
        client.login(username=employee_1.user.username, password='password')
        response = client.get(f'/tasks/{task_1.id}', enforce_csrf_checks=True)
        assert response.status_code == 200
        assert response.context['task'] == task_1

    def test_view_task_form(self, client, task_1, employee_1):
        client.login(username=employee_1.user.username, password='password')
        response = client.get(f'/tasks/{task_1.id}')
        assert isinstance(response.context.get('form'), ViewTaskForm)

    def test_change_status(self, client, task_1, employee_1):
        client.login(username=employee_1.user.username, password='password')
        assert task_1.status == Status.IN_PROGRESS
        client.post(f'/tasks/{task_1.id}', data={'status': 'DONE'})
        updated_task = Task.objects.get(id=task_1.id)
        assert updated_task.status == Status.DONE
