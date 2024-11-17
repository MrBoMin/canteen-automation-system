from django.shortcuts import render
from users.models import User 
from .models import Order

def create_order_view(request):
    user = request.user
    order = Order.objects.create(user=user, status='Pending', total_amount=50.00)
    return render(request, 'orders/order_created.html', {'order': order})