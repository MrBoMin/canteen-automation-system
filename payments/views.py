# payment/views.py

from django.shortcuts import render, redirect
from django.http import JsonResponse
from orders.models import Order
from django.contrib.auth.decorators import login_required

@login_required
def payment_view(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    if order.status != 'Confirmed':
        return redirect('orders:order_summary', order_id=order.id)

    return render(request, 'payments/payment_form.html', {'order': order})

@login_required
def process_payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    # Check if the order is confirmed before allowing payment
    if order.status != 'Confirmed':
        return redirect('orders:order_summary', order_id=order.id)

    payment_method = request.POST.get('payment_method')
    card_number = request.POST.get('card_number', '')
    expiration_date = request.POST.get('expiration_date', '')
    cvv = request.POST.get('cvv', '')

    if payment_method == 'Card Payment' and (card_number and expiration_date and cvv):
        # Simulate card payment here (you can replace this with an actual payment process)
        order.payment_status = True  # Payment completed
        order.payment_method = payment_method
        # No need to change order status to 'Completed' for payment, just for the order process
        order.save()

    elif payment_method == 'Cash on Pickup':
        # For Cash on Pickup, no need to set payment_status to True
        order.payment_status = False  # Payment not completed yet
        order.payment_method = payment_method
        order.save()

    return redirect('orders:order_summary', order_id=order.id)
