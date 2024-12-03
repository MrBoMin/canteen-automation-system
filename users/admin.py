from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User as CUser

# Unregister the default Group and User models
admin.site.unregister(Group)
# admin.site.unregister(User)

# Register your custom User model
@admin.register(CUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
