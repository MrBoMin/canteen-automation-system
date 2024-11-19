from django.db import models
from django.contrib.auth.models import AbstractUser
from menu.models import MenuItem

class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class User(AbstractUser):  # Extending AbstractUser
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    def __str__(self):
        return self.username  # Ensure this only returns the username