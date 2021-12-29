from tasks.models import Task, Comment
import pytest


@pytest.mark.django_db
class TestDeleteTask:
    def test_no_authenticated_user_delete_task(self, client, task_1):
        response = client.get(f'/tasks/delete/{task_1.id}')
        assert response.status_code == 302
        assert response.url == '/'
        Task.objects.get(id=task_1.id)

    @pytest.mark.parametrize('task , user', [('task_1', 'employee_1'), ('task_3', 'manager_1')],
                             ids=['test_employee_delete_task', 'test_manager_different_team_delete_task'])
    def test_account_delete_task(self, request, client, task, user):
        task = request.getfixturevalue(task)
        user = request.getfixturevalue(user)
        client.force_login(user.user)
        response = client.get(f'/tasks/delete/{task.id}')
        assert response.status_code == 302
        assert response.url == '/'
        Task.objects.get(id=task.id)

    def test_manager_delete_task(self, client, manager_1, task_1, comment_1, comment_2):
        client.force_login(manager_1.user)

        comments = Comment.objects.filter(task_id=task_1.id)
        assert comments.exists() is True

        response = client.get(f'/tasks/delete/{task_1.id}')
        assert response.status_code == 302
        assert response.url == '/tasks/'

        with pytest.raises(Exception):
            Task.objects.get(id=task_1.id)

        comments = Comment.objects.filter(task_id=task_1.id)
        assert comments.exists() is False
