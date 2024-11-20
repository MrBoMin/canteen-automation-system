from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from menu.models import MenuItem

# def create_order_view(request):
#     user = request.user
#     order = Order.objects.create(user=user, status='Pending', total_amount=50.00)
#     return render(request, 'orders/order_created.html', {'order': order}) 


@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)

    # Check if the item is in stock
    if menu_item.stock < 1:
        return JsonResponse({'message': 'This item is out of stock!', 'cart_count': 0}, status=400)

    # Check if there is an open order for this user
    order, created = Order.objects.get_or_create(user=request.user, status="Pending")

    # Check if the order item is already in the cart
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        item=menu_item,
        defaults={'price': menu_item.price, 'quantity': 1}
    )

    if not created:
        # If the item is already in the cart, check stock before increasing quantity
        if menu_item.stock >= order_item.quantity + 1:
            order_item.quantity += 1
            order_item.save()
        else:
            return JsonResponse({'message': 'Not enough stock available!', 'cart_count': order.order_items.count()}, status=400)

    return JsonResponse({'message': 'Item added to cart successfully', 'cart_count': order.order_items.count()})



@login_required
def cart_view(request):
    # Fetch the user's cart
    try:
        order = Order.objects.get(user=request.user, status='Pending')
        order_items = order.order_items.select_related('item')
    except Order.DoesNotExist:
        order = None
        order_items = []

    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'orders/cart.html', context)

@login_required
def checkout_view(request):
    try:
        order = Order.objects.get(user=request.user, status='Pending')
        order.status = 'Confirmed'  # Update the status
        order.save()
        # Reduce stock for each order item
        for item in order.order_items.all():
            menu_item = item.item
            menu_item.stock -= item.quantity
            menu_item.save()
        return redirect('orders:order_summary')
    except Order.DoesNotExist:
        return redirect('orders:cart')


@login_required
def order_summary_view(request):
    orders = Order.objects.filter(user=request.user).exclude(status='Pending')
    return render(request, 'order/summary.html', {'orders': orders})

import json

@login_required
@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            # Parse JSON data
            data = json.loads(request.body)
            action = data.get('action')

            # Fetch the specific order item
            order_item = OrderItem.objects.get(id=item_id, order__user=request.user, order__status='Pending')

            # Update quantity based on the action
            if action == 'increase':
                if order_item.item.stock > order_item.quantity:  # Check stock availability
                    order_item.quantity += 1
            elif action == 'decrease':
                if order_item.quantity > 1:  # Ensure quantity doesn't drop below 1
                    order_item.quantity -= 1

            # Save changes and update subtotal
            order_item.save()

            # Recalculate totals for the entire order
            order = order_item.order
            subtotal_all = sum(item.subtotal for item in order.order_items.all())

            return JsonResponse({
                "quantity": order_item.quantity,
                "subtotal": f"{order_item.subtotal:.2f}",
                "subtotal_all": f"{subtotal_all:.2f}",
                "total_all": f"{subtotal_all:.2f}",  # Total matches the subtotal
            })

        except OrderItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            order_item = OrderItem.objects.get(id=item_id, order__user=request.user, order__status='Pending')
            order_item.delete()
            return redirect('orders:cart')
        except OrderItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)