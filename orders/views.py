from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Cart,CartItem
from menu.models import MenuItem
from django.db.models import Sum
import json

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from .models import Order



@login_required
def add_to_cart(request, item_id):
    menu_item = get_object_or_404(MenuItem, id=item_id)

    if menu_item.stock < 1:
        return JsonResponse({'message': 'This item is out of stock!', 'cart_count': 0}, status=400)

    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Add or update the cart item
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        item=menu_item,
        user=request.user,
        defaults={'price': menu_item.price, 'quantity': 1}
    )

    if not created:
        if menu_item.stock >= cart_item.quantity + 1:
            cart_item.quantity += 1
            cart_item.save()
        else:
            return JsonResponse({'message': 'Not enough stock available!', 'cart_count': cart.cart_items.count()}, status=400)

    return JsonResponse({'message': 'Item added to cart successfully', 'cart_count': cart.cart_items.count()})


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    total_amount = sum(item.price * item.quantity for item in cart.cart_items.all())
    context = {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
        'total_amount': total_amount
    }
    return render(request, 'orders/cart.html', context)


@login_required
def make_order(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return redirect('orders:cart')  # Redirect to cart if empty

        # Create a new order
        order = Order.objects.create(user=request.user, status='Pending')

        for cart_item in cart_items:
            # Create order items and deduct stock
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                price=cart_item.item.price,
                quantity=cart_item.quantity
            )
            cart_item.item.stock -= cart_item.quantity
            cart_item.item.save()

        # Clear the cart
        cart_items.delete()

        return redirect(reverse('orders:order_summary', kwargs={'order_id': order.id}))
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



# @login_required
# def checkout_view(request):
#     try:
#         order = Order.objects.get(user=request.user, status='Pending')
#         order.status = 'Confirmed'  # Update the status
#         order.save()
#         # Reduce stock for each order item
#         for item in order.order_items.all():
#             menu_item = item.item
#             menu_item.stock -= item.quantity
#             menu_item.save()
#         return redirect('orders:order_summary')
#     except Order.DoesNotExist:
#         return redirect('orders:cart')




@login_required
def order_summary_view(request, order_id):
    print(order_id)
    # Fetch the specific order using the order_id and ensure it belongs to the logged-in user
    order = Order.objects.filter(user=request.user, id=order_id).first()
    
    if not order:
        # Handle case when no matching order is found, or return a 404
        return render(request, 'orders/order_not_found.html')

    # Calculate the total amount for this specific order
    order.calculate_total_amount()

    return render(request, 'orders/summary.html', {'order': order})


@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            action = data.get('action')
            if action not in ['increase', 'decrease']:
                return JsonResponse({"error": "Invalid action"}, status=400)

            # Fetch the specific cart item
            cart_item = CartItem.objects.get(id=item_id, user=request.user)

            # Perform the action (increase or decrease quantity)
            if action == 'increase':
                if cart_item.item.stock > cart_item.quantity:  # Check stock availability
                    cart_item.quantity += 1
                else:
                    return JsonResponse({"error": "Not enough stock available!"}, status=400)
            elif action == 'decrease':
                if cart_item.quantity > 1:  # Ensure quantity doesn't drop below 1
                    cart_item.quantity -= 1
                else:
                    return JsonResponse({"error": "Quantity cannot be less than 1"}, status=400)

            # Save changes to the cart item
            cart_item.save()

            # Recalculate totals for the entire cart
            subtotal_all = sum(item.subtotal for item in CartItem.objects.filter(user=request.user))

            return JsonResponse({
                "quantity": cart_item.quantity,
                "subtotal": f"{cart_item.subtotal:.2f}",
                "subtotal_all": f"{subtotal_all:.2f}",
                "total_all": f"{subtotal_all:.2f}",
            })

        except CartItem.DoesNotExist:
            return JsonResponse({"error": "Item not found in your cart"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            # Fetch the order item and related order
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart = cart_item.cart

            # Remove the item
            cart_item.delete()

            # Recalculate totals for the order
            subtotal_all = sum(item.subtotal for item in cart.cart_items.all())
            total_all = subtotal_all  # Assuming no additional fees or discounts

            return JsonResponse({
                "message": "Item removed successfully",
                "subtotal_all": f"{subtotal_all:.2f}",
                "total_all": f"{total_all:.2f}",
                "cart_count": cart.cart_items.count()
            })
        except OrderItem.DoesNotExist:
            return JsonResponse({"error": "Item not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)




