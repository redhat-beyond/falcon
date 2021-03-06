from django.db import models
from enumchoicefield import ChoiceEnum, EnumChoiceField
from django.contrib.auth.models import User as DjangoUser
from django.core.validators import validate_email


# Enum
class Role(ChoiceEnum):
    EMPLOYEE = 'Employee',
    MANAGER = 'Manager',


# Create your models here.
class Team(models.Model):
    name = models.CharField(max_length=255, blank=False, unique=True)
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

        User.check_valid_name(first_name)
        User.check_valid_name(last_name)
        validate_email(email)

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

    @staticmethod
    def check_valid_name(string):
        if(len(string) > 30 or not string.isalpha()):
            raise ValueError

    def delete(self, *args, **kwargs):
        self.user.delete()

    def __str__(self) -> str:
        return self.user.username

    def is_employee(self):
        return self.role == Role.EMPLOYEE

    def is_manager(self):
        return self.role == Role.MANAGER
