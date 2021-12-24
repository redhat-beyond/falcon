from tasks.models import Comment, Status, Task
from tasks.forms import CommentForm, ViewTaskForm
import pytest
import random
import string


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

    @pytest.mark.parametrize('form, form_type',
                             [
                                 ('task_form', ViewTaskForm),
                                 ('comment_form', CommentForm),
                             ],
                             ids=[
                                 "task_form",
                                 "comment_form",
                             ])
    def test_view_form(self, client, task_1, employee_1, form, form_type):
        client.login(username=employee_1.user.username, password='password')
        response = client.get(f'/tasks/{task_1.id}')
        assert isinstance(response.context.get(form), form_type)

    def test_change_status(self, client, task_1, employee_1):
        client.login(username=employee_1.user.username, password='password')
        assert task_1.status == Status.IN_PROGRESS
        client.post(f'/tasks/{task_1.id}', data={'taskSubmit': True, 'status': 'DONE'})
        updated_task = Task.objects.get(id=task_1.id)
        assert updated_task.status == Status.DONE

    @pytest.mark.parametrize('content, difference',
                             [
                                ('This is a test comment', 1),
                                ('', 0),
                             ],
                             ids=[
                                "valid_comment_success",
                                "empty_comment_fails",
                             ]
                             )
    def test_add_new_comment(self, client, task_1, employee_1, content, difference):
        client.login(username=employee_1.user.username, password='password')
        current_comments_count = len(task_1.get_comments())
        client.post(f'/tasks/{task_1.id}', data={'commentSubmit': True, 'description': content})
        assert len(task_1.get_comments()) == current_comments_count + difference
        if content == 'This is a test comment':
            last_comment = Comment.objects.filter(task=task_1).order_by('-id')[0]
            assert last_comment.description == content
            assert last_comment.appUser == employee_1
            assert last_comment.task == task_1

    @pytest.mark.parametrize('comment_len',
                             [(10**i) for i in range(0, 5)] + [999],
                             )
    def test_add_new_comment_different_lengths(self, comment_len, client, task_1, employee_1):
        for i in range(10):
            comment_content = ''.join(random.choices(string.ascii_letters + string.punctuation + string.digits,
                                                     k=comment_len))
            current_comments_count = len(task_1.get_comments())
            special_chars = [char for char in comment_content if char in string.punctuation]
            client.login(username=employee_1.user.username, password='password')
            client.post(f'/tasks/{task_1.id}', data={'commentSubmit': True, 'description': comment_content})
            diff = 0 if comment_len > 999 else 1
            assert len(task_1.get_comments()) == current_comments_count + diff, f'Special chars: {special_chars}'
