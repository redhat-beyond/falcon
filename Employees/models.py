from django.db import models
from django.db.models.manager import Manager

class Employees(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employer = models.ForeignKey(Manager)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=True)

