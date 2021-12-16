from django.db.models.query import QuerySet
import pytest
from tasks.models import Comment, Priority, Status, Task
from users.models import Role, User

NUM_COMMENTS_PER_USER = 3


@pytest.mark.django_db
class TestTaskComments:
    @pytest.fixture
    def user_and_manager(self, users):
        user = users[1][0]
        manager = users[2][0]
        assert isinstance(user, User)
        assert isinstance(manager, User)
        assert user.role == Role.EMPLOYEE
        assert manager.role == Role.MANAGER
        assert user.team == manager.team
        return user, manager

    @pytest.fixture
    def task(self, user_and_manager):
        user, manager = user_and_manager
        task = Task.create_task(title='Test task',
                                assignee=user,
                                created_by=manager,
                                priority=Priority.LOW,
                                status=Status.BACKLOG,
                                description='This is a test task')
        return task

    @pytest.fixture
    def comments(self, user_and_manager, task):
        user, manager = user_and_manager
        comments = {}
        for i in range(1, 2 * NUM_COMMENTS_PER_USER + 1):
            comment_user = user if i <= NUM_COMMENTS_PER_USER else manager
            comments[f'comment{i}'] = Comment.objects.create(appUser=comment_user,
                                                             task=task,
                                                             title=f'Comment{i}',
                                                             description='This is a test comment')
        assert len(comments) == 2 * NUM_COMMENTS_PER_USER
        return task

    def test_get_relevant_comments(self, task, comments):
        fetched_comments = task.get_comments()
        assert len(fetched_comments) == 2 * NUM_COMMENTS_PER_USER
        assert isinstance(fetched_comments, QuerySet)
        assert all(isinstance(comment, Comment) for comment in fetched_comments)
        assert all(comment.appUser == task.assignee or comment.appUser == task.created_by
                   for comment in fetched_comments)

    def test_comment_ordered_by_id_ascending(self, task, comments):
        fetched_comments = task.get_comments()
        for i in range(len(fetched_comments) - 1):
            assert fetched_comments[i].id < fetched_comments[i+1].id
