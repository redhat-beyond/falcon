from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.conf import settings
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    role = EnumChoiceField(Role, default=Role.EMPLOYEE, max_length=1)
    team = models.ForeignKey(
        Team, on_delete=models.RESTRICT, related_name='users')

    @staticmethod
    def create_user(username, email, password, first_name, last_name, role, team):
        django_user = DjangoUser.objects.create_user(username=username,
                                                     email=email,
                                                     password=password,
                                                     first_name=first_name,
                                                     last_name=last_name)
        user = User(user=django_user,
                    role=role,
                    team=team)
        user.save()
        return user

    def __str__(self) -> str:
        return self.first_name
