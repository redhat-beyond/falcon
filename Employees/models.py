from django.db import models
<<<<<<< HEAD
from django.db.models.deletion import CASCADE
from Manager.models import Manager


class Employees(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    employer = models.ForeignKey(Manager, on_delete=CASCADE)
    email = models.EmailField(unique=True)
    about = models.TextField(blank=True)
=======

# Create your models here.
>>>>>>> working_branch
