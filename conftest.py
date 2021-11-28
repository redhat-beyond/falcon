import pytest
from users.models import User, Team, Role
from tasks.models import Task, Priority, Status


@pytest.fixture
def teams():
    """
    Adds teams to DB
    """

    return tuple(Team.objects.create(name=f"Team{i}",
                                     description="This is a test team")
                 for i in range(3))


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
        for team in (team1, team2):
            employee = User.create_user(username=f"User{users_counter}",
                                        email=f"User{users_counter}@redhat.com",
                                        password="ssSSAD231!@",
                                        first_name=f"User{users_counter}",
                                        last_name=f"User{users_counter}",
                                        role=Role.EMPLOYEE,
                                        team=team)
            employees.append(employee)
            users_counter += 1
    for i, team in enumerate((team1, team2, team3)):
        manager = User.create_user(username=f"Manager{i}",
                                   email=f"Manager{i}@redhat.com",
                                   password="ssSSAD231!@",
                                   first_name=f"Manager{i}",
                                   last_name=f"Manager{i}",
                                   role=Role.MANAGER,
                                   team=team)
        managers += [manager]
    return teams, tuple(employees), tuple(managers)


@pytest.fixture
def tasks(users):
    """
    Adds tasks to DB
    """
    teams, employees, managers = users
    tasks = []
    for k in range(3):
        for i in range(3):
            for j in range(2):
                task = Task.objects.create(title=f"Task{j}",
                                           assignee=employees[k + i],
                                           created_by=managers[k],
                                           priority=Priority.LOW,
                                           status=Status.BACKLOG,
                                           description="Test task")
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
