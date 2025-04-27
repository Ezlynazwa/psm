from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class Employee(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128, default='defaultpassword')
    position = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    date_hired = models.DateField()
    photo = models.ImageField(upload_to='media/employee_photo/', blank=True, null=True)

    def __str__(self):
        return self.name

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Add related_name to resolve conflicts
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='loginsignup_user_permissions_set',  # Specify a unique reverse accessor name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permisions',
    )
