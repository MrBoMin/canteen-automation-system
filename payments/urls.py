# payment/urls.py

from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('payment/<int:order_id>/', views.payment_view, name='payment_form'),
    path('payment/process/<int:order_id>/', views.process_payment, name='process_payment'),
]
