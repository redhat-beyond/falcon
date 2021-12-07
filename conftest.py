import pytest
from users.models import User, Team, Role
from tasks.models import Comment, Task, Priority, Status
from falcon.test_support import Random


DEFAULT_VALID_PASSWORD = "ssSSAD231!@"
DEFAULT_MAIL_EXTENSION = "@redhat.com"
DEFAULT_DATA_DESCRIPTION = "This is test data"


@pytest.fixture
def teams():
    """
    Adds teams to DB
    """

    return tuple(Team.objects.create(name=f"Team{i}",
                                     description=DEFAULT_DATA_DESCRIPTION)
                 for i in range(1, 4))


@pytest.fixture
def users(teams):
    """
    Adds users to DB
    """
    team1, team2, team3 = teams
    employees = []
    managers = []
    users_counter = 0
    for i in range(3):
        suffix = Random.alphaOnly(i)
        for team in (team1, team2):
            employee = User.create_user(username=f"User{users_counter}",
                                        email=f"User{users_counter}{DEFAULT_MAIL_EXTENSION}",
                                        password=DEFAULT_VALID_PASSWORD,
                                        first_name=f"firstName{suffix}",
                                        last_name=f"lasName{suffix}",
                                        role=Role.EMPLOYEE,
                                        team=team)
            employees.append(employee)
            users_counter += 1
    for i, team in enumerate((team1, team2, team3)):
        suffix = Random.alphaOnly(i)
        manager = User.create_user(username=f"Manager{i}",
                                   email=f"Manager{i}{DEFAULT_MAIL_EXTENSION}",
                                   password=DEFAULT_VALID_PASSWORD,
                                   first_name=f"firstName{suffix}",
                                   last_name=f"lasName{suffix}",
                                   role=Role.MANAGER,
                                   team=team)
        managers.append(manager)
    return teams, tuple(employees), tuple(managers)


@pytest.fixture
def tasks(users):
    """
    Adds tasks to DB
    """
    teams, employees, managers = users
    tasks = []
    tasks_counter = 0
    for team in teams:
        team_employees = User.objects.filter(team=team, role=Role.EMPLOYEE)
        team_manager = User.objects.filter(
            team=team, role=Role.MANAGER).first()
        for employee in team_employees:
            task = Task.objects.create(title=f"Task{tasks_counter}",
                                       assignee=employee,
                                       created_by=team_manager,
                                       priority=Priority.LOW,
                                       status=Status.BACKLOG,
                                       description=DEFAULT_DATA_DESCRIPTION)
            tasks.append(task)
        return teams, employees, managers, tuple(tasks)


@pytest.fixture
def test_db(tasks):
    """
    Returns test DB components as tuples.
    The test DB contains: 3 teams, 3 users per team, 2 tasks per user, 1 manager per team.
    """
    teams = tasks[0]
    employees = tasks[1]
    managers = tasks[2]
    task = tasks[3]
    return teams, employees, managers, task


@pytest.fixture
def valid_teams():
    return [Team.objects.create(name=f"Team{index}", description="Best team ever") for index in range(1, 4)]


@pytest.fixture
def team_1(valid_teams):
    return valid_teams[0]


@pytest.fixture
def employee_1(team_1):
    user = User.create_user(
        username="employee1",
        email="user1@redhat.com",
        password="password",
        first_name="firstName",
        last_name="lastName",
        role=Role.EMPLOYEE,
        team=team_1)
    return user


@pytest.fixture
def manager_1(team_1):
    user = User.create_user(
        username="manager1",
        email="user1@redhat.com",
        password="password",
        first_name="firstName",
        last_name="lastName",
        role=Role.MANAGER,
        team=team_1)
    return user


@pytest.fixture
def task_1(employee_1, manager_1):
    task = Task.objects.create(title="new house",
                               assignee=employee_1,
                               created_by=manager_1,
                               priority=Priority.HIGH,
                               status=Status.IN_PROGRESS,
                               description="build me a house")
    return task


@pytest.fixture
def comment_1(task_1, employee_1):
    comment = Comment.objects.create(appUser=employee_1,
                                     task=task_1,
                                     title="A problem",
                                     description="I dont know how")
    return comment
