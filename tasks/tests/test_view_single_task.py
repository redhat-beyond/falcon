from tasks.models import Comment, Status, Task
from tasks.forms import MAX_COMMENT_LEN, CommentForm, ViewTaskForm
import pytest
import random
import string

VALID_COMMENT_CHARS = string.punctuation + string.digits + string.ascii_letters


@pytest.mark.django_db
class TestViewSingleTask:

    def test_no_authenticated_user_asks_task(self, client, task_1):
        response = client.get(f'/tasks/{task_1.id}')
        assert response.status_code == 302
        assert response.url == '/'

    def test_no_team_account_asks_task(self, client, task_3, employee_1):
        client.force_login(employee_1.user)
        response = client.get(f'/tasks/{task_3.id}')
        assert response.status_code == 302
        assert response.url == '/'

    def test_team_account_asks_task(self, client, task_1, employee_1):
        client.force_login(employee_1.user)
        response = client.get(f'/tasks/{task_1.id}')
        assert response.status_code == 200

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
                                ('a', 1),
                                (''.join(random.choices(string.punctuation, k=1)), 1),
                                (''.join(random.choices(string.punctuation, k=40)), 1),
                                ('a'*MAX_COMMENT_LEN, 1),
                                ('a'*(MAX_COMMENT_LEN + 1), 0),
                                (''.join(random.choices(VALID_COMMENT_CHARS, k=400)), 1),

                             ],
                             ids=[
                                "valid_comment_success",
                                "empty_comment_fails",
                                "single_char_comment_success",
                                "single_special_char_comment_success",
                                "multiple_special_chars_comment_success",
                                "max_len_comment_success",
                                "too_long_comment_fails",
                                "long_comment_success"
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
