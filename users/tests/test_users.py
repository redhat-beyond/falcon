import pytest
from users.models import Role, User
from django.contrib.auth.models import User as DjangoUser
from falcon.test_support import Random


@pytest.mark.django_db
class TestUsers:

    def team(self, team_1):
        return team_1

    def test_create_user(self, employee_1):
        assert isinstance(employee_1, User)
        assert User.objects.filter(user=employee_1.user).exists()

    def test_delete_user(self, employee_1):
        userId = employee_1.user.id
        employee_1.delete()
        assert not User.objects.filter(user=userId).exists()
        assert not DjangoUser.objects.filter(pk=userId).exists()

    failToCreateParams = [
        ('user1', 'password', '', 'first_name', 'last_name', Role.EMPLOYEE, team),
        ('user1', 'password', 'user1@redhat.com', Random.alphaOnly(50), 'lastName', Role.EMPLOYEE, team),
        ('user1', 'password', 'user1@redhat.com', 'firstName', 'lastName', Role.EMPLOYEE, team),
        ('user1', 'password', 'aaaaaa', 'first@Name', 'lastName', Role.EMPLOYEE, team),
        ('user1', 'password', '', 'firstName', 'last@Name', Role.EMPLOYEE, team)
        ]

    @pytest.mark.parametrize('username, password, email, first_name, last_name, role, team', failToCreateParams,
                             ids=["test_create_user_without_email",
                                  "test_create_user_with_long_first_name",
                                  "test_create_user_with_not_valid_email",
                                  "test_create_user_with_special_chars_first_name",
                                  "test_create_user_with_special_chars_last_name"]
                             )
    def test_create_user_without_email(self, username, password, email,
                                       first_name, last_name, role, team):
        with pytest.raises(Exception):
            User.create_user(username, email, password, first_name,
                             last_name, role, team)

    def test_check_is_employee(self, employee_1):
        assert employee_1.is_employee()

    def test_check_is_not_employee(self, manager_1):
        assert not manager_1.is_employee()

    def test_check_is_manager(self, manager_1):
        assert manager_1.is_manager()

    def test_check_is_not_manager(self, employee_1):
        assert not employee_1.is_manager()
