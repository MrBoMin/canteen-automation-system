from django.urls import path
from . import views

app_name = 'menu'  # Namespace for menu app

urlpatterns = [
    path('header.html', views.header_view, name='header'),
    path('footer.html', views.footer_view, name='footer'),
    path('', views.menu_list_view, name='menu_list'),  # Menu page
    path('<int:pk>/', views.menu_detail_view, name='menu_detail')
]