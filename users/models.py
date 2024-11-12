from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class User(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)  # Add this field

    def __str__(self):
        return self.username
