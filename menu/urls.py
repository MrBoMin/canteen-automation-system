from django.urls import path
from . import views

app_name = 'menu'  # Namespace for menu app

urlpatterns = [
    path('<int:pk>/toggle_favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('', views.menu_list_view, name='menu_list'),  # Menu page
    path('<int:pk>/', views.menu_detail_view, name='menu_detail'),
    path('<int:pk>/review/', views.submit_review, name='submit_review')
    
]