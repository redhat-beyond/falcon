from django.db import models

<<<<<<< HEAD

class Manager(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(auto_now=False, auto_now_add=False)
    
=======
# Create your models here.
>>>>>>> working_branch
