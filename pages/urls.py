from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page at root URL
]
