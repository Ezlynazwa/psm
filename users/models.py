from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, default='firstname')
    last_name = models.CharField(max_length=100, default='lastname')
    password = models.CharField(max_length=128, default='defaultpassword')
    position = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    date_hired = models.DateField()
    photo = models.ImageField(upload_to='employee_photo/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

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

class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)

    # Optional additional customer profile info
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='customer_photo/', blank=True, null=True)

    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"