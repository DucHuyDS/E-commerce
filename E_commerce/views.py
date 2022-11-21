from django.shortcuts import render
from store.models import Product,Category
# Create your views here.

def home(request):
    products=Product.objects.all().filter(is_active=True).order_by('-created_at')[:8]
    product_recommend=Product.objects.all().filter(is_active=True).order_by('-sold')[:8]
    context={
        'products':products,
        'product_recommend':product_recommend,
        
    }
    return render(request,'home.html',context)