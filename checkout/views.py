
from django.shortcuts import render
from cart.models import CartItem, Cart
from accounts.models import AccountProfile
from .models import Payment, Order, Contact,Discount
from django.http import JsonResponse
from store.models import Product
import json
from django.contrib import messages
from accounts.forms import AccountForm,AccountProfileForm
# Create your views here.


def checkout(request, price=0,discount=0, tax=0, total_price=0):
    user=request.user
    user_profile=AccountProfile.objects.get(user_id=user.id)
    accountform=AccountForm(instance=user)
    profileform=AccountProfileForm(instance=user_profile)
    if request.method == 'POST':
        get_discount=request.POST['discount'].rstrip()
        try:
            discount_name=Discount.objects.get(name__exact=get_discount)
            discount=discount_name.price
            
            messages.success(request,'Áp mã thành công')
        except Discount.DoesNotExist:
            messages.error(request,'Mã không hợp lệ')
    cart = Cart.objects.get(user=user)
    user_profile = AccountProfile.objects.get(user=user)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        price += cart_item.sub_total()
    tax = price/100
    discount=price*discount
    total_price = price+tax-discount
    if total_price <=0:
        total_price=0.5
    context = {
        'cart_items': cart_items,
        'user_profile': user_profile,
        'price': price,
        'tax': tax,
        'total_price': round(total_price,2),
        'discount': round(discount,2),
        'accountform':accountform,
        'profileform':profileform
    }
    return render(request, 'checkout/checkout.html', context)


def payment(request):
    user=request.user
    user.notification+=1
    user.save()

    # user.
    body = json.loads(request.body)
    payment = Payment(user_id=request.user.id, payment_id=body['payment_id'], status=body['status'],
                      created_at=body['created_at'], updated_at=body['updated_at'], price=body['price'], tax=body['tax'], total_price=body['total_price'], discount=body['discount'])
    payment.save()
    user_profile = AccountProfile.objects.get(user_id=request.user.id)
    contact = Contact(user_id=request.user.id,
                      phone=request.user.phone, full_name=request.user.full_name(), address=user_profile.address, payment=payment)
    contact.save()
    
    cart = Cart.objects.get(user_id=request.user.id)
    cart_items = CartItem.objects.filter(cart=cart, is_active=True)
    for cart_item in cart_items:
        order = Order()
        order.user_id = request.user.id
        order.payment = payment
        order.product_id = cart_item.product.id
        order.quantity=cart_item.quantity
        order.sub_total=cart_item.sub_total()
        order.save()
        order.variations.set(cart_item.variations.all())
        order.is_ordered = True
        order.save()
        product = Product.objects.get(id=cart_item.product.id)
        product.stock -= cart_item.quantity
        product.sold+=cart_item.quantity
        product.save()
    cart_items.delete()
    data = {
        'payment_id': payment.payment_id,
    }
    return JsonResponse(data)


def order_complete(request):
    payment_id = request.GET.get('payment_id')
    payment = Payment.objects.get(payment_id=payment_id)
    order = Order.objects.filter(payment=payment)
    contact=Contact.objects.get(payment=payment)
    context = {
        'contact': contact,
        'order': order,
    }
    return render(request, 'checkout/order_complete.html', context)
