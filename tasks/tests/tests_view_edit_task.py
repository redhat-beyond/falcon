from tasks.forms import TaskForm
from tasks.models import Task
import pytest


@pytest.mark.django_db
class TestViewEditTask:
    def test_no_authenticated_edit_task(self, client):
        response = client.get(f'/tasks/edit/{1}')
        assert response.status_code == 200
        assert 'not_auth_user' in response.context.keys()

    def test_employee_edit_task(self, client, employee_1):
        client.login(username=employee_1.user.username, password='password')
        response = client.get(f'/tasks/edit/{1}')
        assert response.status_code == 200
        assert 'not_auth_user' not in response.context.keys()

    def test_manager_edit_task(self, client, manager_1, task_1):
        client.login(username=manager_1.user.username, password='password')
        response = client.get(f'/tasks/edit/{task_1.id}')
        assert response.status_code == 200
        assert 'form' in response.context.keys()

    def test_view_edit_task_form(self, client, manager_1, task_1):
        client.force_login(manager_1.user)
        response = client.get(f'/tasks/edit/{task_1.id}')
        assert response.status_code == 200
        assert isinstance(response.context.get('form'), TaskForm)

    def test_load_edit_view(self, client, manager_1, task_2, task_2_data):
        client.force_login(manager_1.user)
        response = client.get(f'/tasks/edit/{task_2.id}')
        assert response.status_code == 200
        form_load_data = response.context['form'].initial
        assert form_load_data['title'] == task_2_data['title']
        assert form_load_data['assignee'] == task_2_data['assignee']
        assert form_load_data['created_by'] == task_2_data['created_by']
        assert form_load_data['description'] == task_2_data['description']
        assert str(form_load_data['status']).upper() == task_2_data['status']
        assert str(form_load_data['priority']).upper() == task_2_data['priority']

    def test_edit_task_valid(self, client, manager_1, task_2, task_2_data, employee_11):
        client.force_login(manager_1.user)
        task_2_data['assignee'] = employee_11.user.id
        task_2_data['description'] = 'this is the new des'
        task_2_data['status'] = 'DONE'
        task_2_data['created_by'] = manager_1.user.id
        response = client.post(f'/tasks/edit/{task_2.id}', data=task_2_data)
        assert response.status_code == 302
        assert response.url == f'/tasks/{task_2.id}'
        task_2_from_DB = Task.objects.get(id=task_2.id)
        assert task_2_from_DB.title == task_2_data['title']
        assert task_2_from_DB.assignee.user.id == task_2_data['assignee']
        assert task_2_from_DB.created_by.user.id == task_2_data['created_by']
        assert task_2_from_DB.description == task_2_data['description']
        assert str(task_2_from_DB.status).upper() == task_2_data['status']
        assert str(task_2_from_DB.priority).upper() == task_2_data['priority']

    @pytest.mark.parametrize('field', ['status', 'priority' ,'assignee' , 'created_by' ])
    def test_edit_task_invalid(self, client, manager_1, task_2, task_2_data ,field):
        client.force_login(manager_1.user)
        task_2_data[field] = 'RANDOM'
        with pytest.raises(ValueError):
            client.post(f'/tasks/edit/{task_2.id}', data=task_2_data)



