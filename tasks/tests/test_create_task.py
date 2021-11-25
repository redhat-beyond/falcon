import pytest
from tasks.models import Priority, Status, Task
from users.models import User, Team, Role
from django.contrib.auth.models import User as DjangoUser


@pytest.mark.django_db
class TestCreateTask:
    """
    Add test team to DB
    """
    @pytest.fixture
    def team(self):
        team = Team(name="TestTeam",
                    description="This is a test team")
        team.save()
        return team

    """
    Add another test team to DB
    """
    @pytest.fixture
    def other_team(self):
        team = Team(name="TestOtherTeam",
                    description="This is a test team")
        team.save()
        return team

    """
    Add manager user to the DB
    """
    @pytest.fixture
    def manager(self, team):
        django_user = DjangoUser.objects.create_user(username="TestManager",
                                                     email="example@gmail.com",
                                                     password='xsdDS23',
                                                     first_name="Test",
                                                     last_name="Test")
        manager = User.objects.create(user=django_user,
                                      role=Role.MANAGER,
                                      team=team)
        manager.save()
        return manager

    """
    Add an employee to the team in "team" fixture
    """
    @pytest.fixture
    def employee(self, team):
        django_user = DjangoUser.objects.create_user(username="TestEmployee",
                                                     email="example@gmail.com",
                                                     password='xsdDS23',
                                                     first_name="Test",
                                                     last_name="Test")
        employee = User.objects.create(user=django_user,
                                       role=Role.EMPLOYEE,
                                       team=team)
        employee.save()
        return employee

    """
    Add an employee to the team in "other_team" fixture
    """
    @pytest.fixture
    def employee_other_team(self, other_team):
        django_user = DjangoUser.objects.create_user(username="TestEmployee",
                                                     email="example@gmail.com",
                                                     password='xsdDS23',
                                                     first_name="Test",
                                                     last_name="Test")
        employee = User.objects.create(user=django_user,
                                       role=Role.EMPLOYEE,
                                       team=other_team)
        employee.save()
        return employee

    """
    Test add new task
    """
    def test_add_task_to_db(self, manager, employee):
        Task.create_task(title="TestTask",
                         assignee=employee,
                         assigner=manager,
                         priority=Priority.CRITICAL,
                         status=Status.BACKLOG,
                         description="This is a test task")
        assert len(Task.objects.all()) == 1

    """
    Test that a user who is not manager cannot assign task to other
    teams employees.
    """
    def test_assigned_by_non_manager(self, manager, employee):
        assert employee.role != Role.MANAGER
        with pytest.raises(ValueError):
            Task.create_task(title="TestTask",
                             assignee=manager,
                             assigner=employee,
                             priority=Priority.CRITICAL,
                             status=Status.BACKLOG,
                             description="This is a test task")
        assert len(Task.objects.all()) == 0

    """
    Test that title is required when creating a task.
    """
    def test_no_title(self, manager, employee):
        with pytest.raises(ValueError):
            Task.create_task(title="",
                             assignee=employee,
                             assigner=manager,
                             priority=Priority.CRITICAL,
                             status=Status.BACKLOG,
                             description="This is a test task")
        assert len(Task.objects.all()) == 0

    """
    Test that priority must be a valid enum value
    """
    def test_invalid_priority(self, manager, employee):
        with pytest.raises(ValueError):
            Task.create_task(title="TestTask",
                             assignee=employee,
                             assigner=manager,
                             priority='INVALID',
                             status=Status.BACKLOG,
                             description="This is a test task")
        assert len(Task.objects.all()) == 0

    """
    Test that status must be a valid enum value
    """
    def test_invalid_status(self, manager, employee):
        with pytest.raises(ValueError):
            Task.create_task(title="TestTask",
                             assignee=employee,
                             assigner=manager,
                             priority=Priority.CRITICAL,
                             status='INVALID',
                             description="This is a test task")
        assert len(Task.objects.all()) == 0

    """
    Test that manager cannot assign task to other teams employees
    """
    def test_assign_other_team(self, manager, employee_other_team):
        with pytest.raises(ValueError):
            Task.create_task(title="TestTask",
                             assignee=employee_other_team,
                             assigner=manager,
                             priority=Priority.CRITICAL,
                             status=Status.BACKLOG,
                             description="This is a test task")
        assert len(Task.objects.all()) == 0
