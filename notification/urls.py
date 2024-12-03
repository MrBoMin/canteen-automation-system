# urls.py
from django.urls import path
from . import views
app_name = 'notifications'

urlpatterns = [
  path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
]