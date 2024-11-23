from .models import Cart

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
