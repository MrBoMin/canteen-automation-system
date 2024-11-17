from django.db import models

class Role(models.Model):
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return self.role_name

class User(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    bio = models.TextField(blank=True, null=True)  # Optional bio for users
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Path to profile pictures

    def __str__(self):
        return self.username
