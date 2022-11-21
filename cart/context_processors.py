from .models import  CartItem,Cart

def counter(request,cart_count=0):
    if request.user.is_authenticated:
        try:
            cart=Cart.objects.get(user=request.user)
            cart_items=CartItem.objects.filter(cart=cart)
            for item in cart_items:
                cart_count+=item.quantity
        except Cart.DoesNotExist:
            cart_count=0
    return dict(cart_count=cart_count)