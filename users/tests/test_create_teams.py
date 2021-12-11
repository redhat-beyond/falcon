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
            Team.objects.create(title="", description="Best team ever")

    @pytest.mark.django_db(transaction=True)
    def test_create_team_with_same_name(self):
        assert len(Team.objects.all()) == 0
        Team.objects.create(name="Team1", description="This team will be created")
        assert len(Team.objects.all()) == 1
        with pytest.raises(Exception):
            Team.objects.create(name="Team1", description="This team will be created")
        assert len(Team.objects.all()) == 1, "Team1 was created twice"
