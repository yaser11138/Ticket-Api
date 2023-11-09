from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    pass


class Staff(MyUser):
    department_section = models.CharField(max_length=30)