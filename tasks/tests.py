from tasks.models import Status, Priority, Task
import pytest
from users.models import Role, User, Team


@pytest.mark.django_db
class TestTasks:

    @pytest.fixture
    def team1(self):
        team_1 = Team.objects.create(
            name="Team1", description="Best team ever")
        return team_1

    @pytest.fixture
    def employee(self, team1):
        user = User.create_user(
            username="employee",
            email="user1@redhat.com",
            password="password",
            first_name="first_name",
            last_name="last_name",
            role=Role.EMPLOYEE,
            team=team1)
        return user

    @pytest.fixture
    def manager(self, team1):
        user = User.create_user(
            username="manager",
            email="user1@redhat.com",
            password="password",
            first_name="first_name",
            last_name="last_name",
            role=Role.MANAGER,
            team=team1)
        return user

    @pytest.fixture
    def task1(self, employee, manager):
        task = Task.objects.create(title="TestTask",
                                   assignee=employee,
                                   created_by=manager,
                                   priority=Priority.CRITICAL,
                                   status=Status.BACKLOG,
                                   description="This is a test task")
        return task

    def test_update_status(self, task1):
        task1.update_status(Status.DONE)
        assert Task.objects.get(pk=task1.id).status == Status.DONE

    def test_update_priority(self, task1):
        task1.update_priority(Priority.LOW)
        assert Task.objects.get(pk=task1.id).priority == Priority.LOW
