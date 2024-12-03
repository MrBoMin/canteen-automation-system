from django.urls import path
from . import views  # Import your views here
from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name="profile"),
    path('users/logout/', views.logout_view, name='logout'),
    path('profile/edit/<int:user_id>/', views.edit_user_info, name='edit_user_info'),
    path('profile/my-orders/', views.my_orders, name='my_orders'),
    path('profile/order-history/', views.order_history, name='order-history'),
    path('change-password/', views.change_password, name='change_password'),
]
