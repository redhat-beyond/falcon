from tasks.models import Comment, Status, Priority, Task
import pytest
from users.models import Role, User, Team


@pytest.mark.django_db
class TestComments:

    @pytest.fixture
    def team_1(self):
        return Team.objects.create(name="Team1", description="Best team ever")

    @pytest.fixture
    def employee_1(self, team_1):
        user = User.create_user(
            username="employee1",
            email="user1@redhat.com",
            password="password",
            first_name="first_name",
            last_name="last_name",
            role=Role.EMPLOYEE,
            team=team_1)
        return user

    @pytest.fixture
    def manager_1(self, team_1):
        user = User.create_user(
            username="manager1",
            email="user1@redhat.com",
            password="password",
            first_name="first_name",
            last_name="last_name",
            role=Role.MANAGER,
            team=team_1)
        return user

    @pytest.fixture
    def task_1(self, employee_1, manager_1):
        task = Task.objects.create(title="new house",
                                   assignee=employee_1,
                                   created_by=manager_1,
                                   priority=Priority.HIGH,
                                   status=Status.IN_PROGRESS,
                                   description="build me a house")
        return task

    @pytest.fixture
    def comment_1(self, task_1, employee_1):
        comment = Comment.objects.create(appUser=employee_1,
                                         task=task_1,
                                         title="A problem",
                                         description="I dont know how")
        return comment

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

    def test_update_status(self, task_1):
        task_1.update_status(Status.DONE)
        assert task_1.status == Status.DONE
        assert Task.objects.get(pk=task_1.id).status == Status.DONE

    def test_update_priority(self, task_1):
        task_1.update_priority(Priority.LOW)
        assert task_1.priority == Priority.LOW
        assert Task.objects.get(pk=task_1.id).priority == Priority.LOW
