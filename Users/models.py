from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        # creating different kinds of users
        ADMIN = "ADMIN",'Admin'
        TEACHER = "TEACHER",'Teacher'
        STUDENT = "STUDENT",'Student'
    base_role = Role.ADMIN # by default the user is admin