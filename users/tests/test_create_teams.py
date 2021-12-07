import pytest
from users.models import Team


@pytest.mark.django_db
class TestTeams:

    def test_create_teams(self, valid_teams):
        for team in valid_teams:
            assert isinstance(team, Team)
            assert Team.objects.filter(id=team.id).exists()

    def test_create_team_without_title(self):
        with pytest.raises(Exception):
            Team.objects.create(description="Best team ever")
