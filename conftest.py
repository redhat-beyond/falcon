import pytest
from users.models import Role, User, Team


@pytest.fixture
def new_team_factory(db):
    def create_team(name="Team1",
                    description="very good team"):
        team = Team.objects.create(name=name,
                                   description=description)
        return team
    return create_team


@pytest.fixture
def team_1(db, new_team_factory):
    return new_team_factory()


@pytest.fixture
def new_user_factory(db, new_team_factory):
    def create_user(username="username",
                    email="username@redhat.com",
                    password="password",
                    first_name="first_name",
                    last_name="last_name",
                    role=Role.EMPLOYEE,
                    team=new_team_factory("Team1", "Best team")):
        user = User.create_user(username=username,
                                email=email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                role=role,
                                team=team)
        return user
    return create_user


@pytest.fixture
def employee_1(db, new_user_factory):
    return new_user_factory()
