from tasks.models import Comment
import pytest


@pytest.mark.django_db
class TestComments:

    def test_create_comment(self, comment_1):
        assert isinstance(comment_1, Comment)
        assert Comment.objects.filter(id=comment_1.id).exists()

    def test_user_make_two_comments(self, task_1, employee_1, comment_1):
        com = Comment.objects.create(appUser=employee_1,
                                     title="A problem2",
                                     task=task_1,
                                     description="Need more info")
        assert com.id != comment_1.id

    def test_comment_without_title(self, task_1, employee_1):
        with pytest.raises(Exception):
            Comment.objects.create(appUser=employee_1,
                                   task=task_1,
                                   description="Need more info")
