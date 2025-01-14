from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    date_hired = models.DateField()
    photo = models.ImageField(upload_to='media/employee_photo/', blank=True, null=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Add related_name to resolve conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='loginsignup_user_set',  # Specify a unique reverse accessor name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='loginsignup_user_permissions_set',  # Specify a unique reverse accessor name
        blank=True
    )
