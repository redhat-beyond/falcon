from django.test import TestCase
from users.models import Role, User, Team


class TestUserModel(TestCase):

    def test_create_user(self):
        username = "username"
        password = "password"
        email = "user@example.com"
        first_name = "first_name"
        last_name = "last_name"
        name = "Alpha"
        description = "best team ever"
        team = Team.objects.create(name=name, description=description)
        user = User.create_user(
            username, email, password, first_name, last_name, Role.EMPLOYEE, team)
        assert isinstance(user, User)
        assert user.user.first_name == first_name


class TestTeamModel(TestCase):

    def test_create_team(self):
        name = "Alpha"
        description = "best team ever"
        team = Team.objects.create(name=name, description=description)
        assert isinstance(team, Team)
        assert team.name == name
        assert team.description == description
