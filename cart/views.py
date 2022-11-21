from email import message
from django.shortcuts import redirect, render
from store.models import Product,Variation
from checkout.models import  Discount
from .models import CartItem,Cart
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url='log_in')
def cart(request,price=0,discount=0,tax=0,total_price=0):
    if request.method == 'POST':
        get_discount=request.POST['discount'].rstrip()
        try:
            discount_name=Discount.objects.get(name__exact=get_discount)
            discount=discount_name.price
            messages.success(request,'Áp mã thành công')
        except Discount.DoesNotExist:
            messages.error(request,'Mã không hợp lệ')
    cart=Cart.objects.get(user=request.user)
    cart_items=CartItem.objects.filter(cart=cart)
    cart_items_active=CartItem.objects.filter(cart=cart,is_active=True)
    for item in cart_items_active:
        # if item.is_active==True:
        price+=item.product.price*item.quantity
    tax=price/100
    discount=price*discount
    total_price=price+tax-discount 
    context={
        'cart_items':cart_items,
        'cart_items_active':cart_items_active,
        'price':price,
        'tax':tax,
        'total_price': round(total_price,2),
        'discount': round(discount,2),
    }

    return render(request,'store/cart.html',context)

@login_required(login_url='log_in')
def add_cart(request,product_id, buynow=None,quantity=1):
    product=Product.objects.get(id=product_id)
    url=request.META.get('HTTP_REFERER')
    if request.method=="POST":
        product_variation=[]
        for item in request.POST:
            key=item
            value=request.POST[item]
            try:
                variation=Variation.objects.get(product=product,variation_caterogy__iexact=key,variation_value=value)
                product_variation.append(variation)
            except:
                if key == 'quantity':
                    quantity=int(request.POST[item])
         
                    if quantity > product.stock:
                        messages.error(request,'Vượt quá số lượng')
                        return redirect(url)

                   

        cart=Cart.objects.get(user=request.user)
        cart_items_exists=CartItem.objects.filter(product=product,cart=cart).exists()
        
        if cart_items_exists:
            variation_list=[]
            product_id=[]
            total_quantity=0
            cart_items=CartItem.objects.filter(product=product,cart=cart)
            for item in cart_items:
                variation_list.append(list(item.variations.all()))
                product_id.append(item.id)
                total_quantity+=item.quantity
            if quantity+total_quantity > product.stock:
                messages.error(request,'Số lượng sản phẩm này đã đạt đến giới hạn')
                return redirect(url)
            elif product_variation in variation_list:
                index=variation_list.index(product_variation)
                item_id=product_id[index]
                cart_items=CartItem.objects.get(id=item_id,product=product,cart=cart)
                cart_items.quantity+=quantity
                cart_items.save()
                
                # return redirect(url)
            else:
                cart_items=CartItem.objects.create(product=product,cart=cart,quantity=quantity)
                cart_items.variations.add(*product_variation)
                cart_items.save()
                # return redirect(url)
        else:
            cart_items=CartItem.objects.create(product=product,cart=cart,quantity=quantity)
            cart_items.variations.add(*product_variation)
            cart_items.save()
            # return redirect(url)

    if buynow:
        return redirect('cart')
    if '/cart/' not in url:
        messages.success(request,'Thêm vào giỏ hàng thành công') 
    return redirect(url)

def remove_cart_item(request,product_id,cart_item_id):
    product=Product.objects.get(id=product_id)
    cart_item=CartItem.objects.get(id=cart_item_id,product=product)
    if cart_item.quantity > 1:
        cart_item.quantity-=1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

def delete_cart_item(request,product_id,cart_item_id):
    product=Product.objects.get(id=product_id)
    cart_item=CartItem.objects.get(id=cart_item_id,product=product)
    cart_item.delete()
    
    return redirect('cart')

def active_cart_item(request,cart_item_id):
    cart_item=CartItem.objects.get(id=cart_item_id)
    
    cart_item.is_active=True
    cart_item.save()
    return redirect('cart')

def inactive_cart_item(request,cart_item_id):
    cart_item=CartItem.objects.get(id=cart_item_id)
   
    cart_item.is_active=False
    cart_item.save() 
    return redirect('cart')