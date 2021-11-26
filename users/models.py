from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.contrib.auth.models import User as DjangoUser


# Enum
class Role(ChoiceEnum):
    EMPLOYEE = 'Employee',
    MANAGER = 'Manager',


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name


class User(models.Model):
    user = models.OneToOneField(
        DjangoUser, on_delete=models.CASCADE, primary_key=True)
    role = EnumChoiceField(Role, default=Role.EMPLOYEE, max_length=1)
    team = models.ForeignKey(
        Team, on_delete=models.RESTRICT, related_name='team')

    @staticmethod
    def create_user(username, email, password, first_name, last_name, role, team):
        django_user = DjangoUser.objects.create_user(username=username,
                                                     email=email,
                                                     password=password,
                                                     first_name=first_name,
                                                     last_name=last_name)
        if isinstance(django_user, DjangoUser):
            user = User.objects.create(user=django_user,
                                       role=role,
                                       team=team)
            return user
        else:
            raise Exception("Error creating user")

    def delete(self, *args, **kwargs):
        self.user.delete()

    def __str__(self) -> str:
        return self.user.username

    def get_user_role(self):
        return self.role

    @staticmethod
    def is_employee(user):
        if user.get_user_role() == Role.EMPLOYEE:
            return True
        else:
            return False

    @staticmethod
    def is_manager(user):
        if user.get_user_role() == Role.MANAGER:
            return True
        else:
            return False
