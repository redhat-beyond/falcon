from users.models import *
from tasks.models import *
from django.contrib.auth.models import User as DjangoUser


class Demo():

    def __init__(self) -> None:
        pass

    def create(self):
        self.managersTeam = Team.objects.create(
            name="Managers", description="control all")
        self.employeesTeam = Team.objects.create(
            name="Employees", description="doing all")

        self.managers = [User.create_user(f"user{i}", f"user{i}@redhat.com", "Aa12345",
                                          f"Paul", f"Cormier", Role.MANAGER, self.managersTeam) for i in range(3)]

        self.employees = [User.create_user(f"user{i}", f"user{i}@redhat.com",
                                           "Aa12345", f"Elon", f"Musk", Role.EMPLOYEE, self.employeesTeam) for i in range(3, 6)]

    def delete(self):
        User.objects.all().delete()
        Team.objects.all().delete()
        DjangoUser.objects.all().delete()


demo = Demo()
