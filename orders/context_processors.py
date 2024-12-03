from .models import Cart
from notification.models import Notification


def cart_count(request):
    """
    Context processor to add the cart count to all templates.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            return {'cart_count': cart.cart_items.count()}
        except Cart.DoesNotExist:
            return {'cart_count': 0}
    return {'cart_count': 0}




def base_view(request):
    notifications = []
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user, status='Unread').order_by('-created_at')[:5]
    
    return {
        'notifications': notifications
    }
