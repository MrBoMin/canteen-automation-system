from django.db import models
from django.contrib.auth.models import AbstractUser
from menu.models import MenuItem

class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class User(AbstractUser):  # Extending AbstractUser
    email = models.EmailField(unique=True)  # Ensure the email is unique
    USERNAME_FIELD = 'email'  # Make email the username field
    REQUIRED_FIELDS = ['username']  # Add other fields if needed
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, default='default_profile.webp')


    def __str__(self):
        return self.username  # Ensure this only returns the username