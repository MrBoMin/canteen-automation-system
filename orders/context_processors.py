from .models import Order

def cart_count(request):
    """
    Context processor to add the cart count to all templates.
    """
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(user=request.user, status='Pending')
            return {'cart_count': order.order_items.count()}
        except Order.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0}
