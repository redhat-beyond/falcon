import pytest
from tasks.models import Priority, Status, Task
from users.models import User, Team, Role


@pytest.mark.django_db
class TestCreateTask:
    """
    Add test team to DB
    """
    @pytest.fixture
    def team(self):
        team = Team.objects.create(name="TestTeam",
                                   description="This is a test team")
        return team

    """
    Add another test team to DB
    """
    @pytest.fixture
    def other_team(self):
        team = Team.objects.create(name="TestOtherTeam",
                                   description="This is a test team")
        return team

    """
    Add manager user to the DB
    """
    @pytest.fixture
    def manager(self, team):
        manager = User.create_user(username="TestManager",
                                   email="example@gmail.com",
                                   password='xsdDS23',
                                   first_name='Test',
                                   last_name='Test',
                                   role=Role.MANAGER,
                                   team=team)
        return manager

    """
    Add an employee to the team in "team" fixture
    """
    @pytest.fixture
    def employee(self, team):
        employee = User.create_user(username="TestEmployee",
                                    email="example@gmail.com",
                                    password='xsdDS23',
                                    first_name='Test',
                                    last_name='Test',
                                    role=Role.EMPLOYEE,
                                    team=team)
        return employee

    """
    Add an employee to the team in "other_team" fixture
    """
    @pytest.fixture
    def employee_other_team(self, other_team):
        employee = User.create_user(username="TestEmployee",
                                    email="example@gmail.com",
                                    password='xsdDS23',
                                    first_name='Test',
                                    last_name='Test',
                                    role=Role.EMPLOYEE,
                                    team=other_team)
        return employee

    @pytest.mark.parametrize('title, assignee, assigner, priority, status, description, length', [
                            ('TestTask', 'employee', 'manager', Priority.CRITICAL, Status.BACKLOG,
                             'This is description', 1),
                            ('TestTask', 'manager', 'employee', Priority.CRITICAL, Status.BACKLOG,
                             'This is description', 0),
                            ('', 'employee', 'manager', Priority.CRITICAL, Status.BACKLOG,
                             'This is description', 0),
                            ('TestTask', 'employee', 'manager', 'INVALID', Status.BACKLOG,
                             'This is description', 0),
                            ('TestTask', 'employee', 'manager', Priority.CRITICAL, 'INVALID',
                             'This is description', 0),
                            ('TestTask', 'employee_other_team', 'manager', Priority.CRITICAL, Status.BACKLOG,
                             'This is description', 0),
                        ],
                            ids=[
                                "test_add_task_to_db",
                                "test_assigned_by_non_manager",
                                "test_no_title",
                                "test_invalid_priority",
                                "test_invalid_status",
                                "test_assign_other_team",
                            ]
                        )
    def test_create_task(self, request, title, assignee, assigner, priority, status, description, length):
        assignee = request.getfixturevalue(assignee)
        created_by = request.getfixturevalue(assigner)
        try:
            Task.create_task(title=title,
                             assignee=assignee,
                             created_by=created_by,
                             priority=priority,
                             status=status,
                             description=description)
        except ValueError:
            pass
        assert len(Task.objects.all()) == length
