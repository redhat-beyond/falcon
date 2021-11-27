import pytest
from users.models import Role, User, Team
from django.contrib.auth.models import User as DjangoUser


@pytest.mark.django_db
class TestTeams:

    @pytest.fixture
    def valid_teams(self):
        team_1 = Team.objects.create(
            name="Team1", description="Best team ever")
        team_2 = Team.objects.create(
            name="Team2", description="Best team ever")
        team_3 = Team.objects.create(
            name="Team3", description="Best team ever")
        return team_1, team_2, team_3

    def test_create_teams(self, valid_teams):
        for team in valid_teams:
            assert isinstance(team, Team)
            assert Team.objects.filter(id=team.id).exists()

    def test_create_team_without_title(self):
        with pytest.raises(Exception):
            Team.objects.create(description="Best team ever")


@pytest.mark.django_db
class TestUsers:

    @pytest.fixture
    def team_1(self):
        return Team.objects.create(name="Team1", description="Best team ever")

    @pytest.fixture
    def employee_1(self, team_1):
        user1 = User.create_user(
            username="user1",
            email="user1@redhat.com",
            password="password",
            first_name="first_name",
            last_name="last_name",
            role=Role.EMPLOYEE,
            team=team_1)
        return user1

    def test_create_user(self, employee_1):
        assert isinstance(employee_1, User)
        assert User.objects.filter(user=employee_1.user).exists()

    def test_delete_user(self, employee_1):
        userId = employee_1.user.id
        employee_1.delete()
        assert not User.objects.filter(user=userId).exists()
        assert not DjangoUser.objects.filter(pk=userId).exists()

    def test_create_user_without_email(self):
        with pytest.raises(Exception):
            User.create_user(
                username="user1",
                password="password",
                first_name="first_name",
                last_name="last_name",
                role=Role.EMPLOYEE,
                team=TestTeams.valid_team)

    def test_create_user_with_long_name(self):
        longName = """ this is a very
        long string if I had the
        energy to type more and more ..."""
        with pytest.raises(Exception):
            User.create_user(
                username="user1",
                email="user1@redhat.com",
                password="password",
                first_name=longName,
                last_name="last_name",
                role=Role.EMPLOYEE,
                team=TestTeams.valid_team)
