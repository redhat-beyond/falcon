from django.db import models
from django.conf import settings


# Enums
class Roles(models.TextChoices):
    EMPLOYEE = 'E', 'Employee'
    MANAGER = 'M', 'Manager'


# Create your models here.
class Teams(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name


class User(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=1, choices=Roles.choices, default=Roles.EMPLOYEE)
    team_id = models.ForeignKey(Teams, on_delete=models.RESTRICT, related_name='users')

    def __str__(self) -> str:
        return self.first_name
