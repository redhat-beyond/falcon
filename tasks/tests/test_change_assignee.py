import pytest
from tasks.models import Task
from users.models import Team, User


@pytest.mark.django_db
class TestChangeTaskAssignee:
    def test_change_task_assignee(self, test_db):
        team = test_db[0][0]
        employee_1, employee_2 = User.objects.filter(team=team)[:2]
        task = Task.objects.filter(assignee=employee_1).first()
        assert task is not None
        assert task.assignee == employee_1
        task.change_assignee(employee_2)
        assert task.assignee == employee_2
    
    @pytest.mark.parametrize("invalid_input", ["INVALID VALUE", None, 2])
    def test_change_assignee_invalid_input(self, test_db, invalid_input):
        _, _, _, tasks = test_db
        task = tasks[0]
        assignee = task.assignee
        with pytest.raises(Exception):
            task.change_assignee(invalid_input)
        assert assignee == task.assignee

    def test_change_assignee_other_team(self, test_db):
        teams = Team.objects.all()
        assert len(teams) > 0
        team_1 = teams[0]
        team_2 = teams[1]
        employee_1 = User.objects.filter(team=team_1).first()
        employee_2 = User.objects.filter(team=team_2).first()
        task = Task.objects.filter(assignee=employee_1).first()
        with pytest.raises(Exception):
            task.change_assignee(employee_2)
        assert task.assignee == employee_1

