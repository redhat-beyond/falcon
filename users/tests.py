from users.models import Role, User, Team


def test_create_user(employee_1):
    assert isinstance(employee_1, User)
    assert employee_1.role == Role.EMPLOYEE


def test_create_team(team_1):
    assert isinstance(team_1, Team)
    assert team_1.name == "Team1"
