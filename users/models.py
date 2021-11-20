from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.conf import settings


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
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = EnumChoiceField(Role, default=Role.EMPLOYEE, max_length=1)
    team_id = models.ForeignKey(
        Team, on_delete=models.RESTRICT, related_name='users')

    def __str__(self) -> str:
        return self.first_name
