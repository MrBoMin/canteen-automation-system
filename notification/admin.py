from django.contrib import admin
from .models import Notification



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'order', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__username', 'order__orderid')