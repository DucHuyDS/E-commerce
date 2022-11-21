
from django.shortcuts import redirect, render
from store.forms import ReviewForm
from .models import Product,ReviewRating,Brand,ProductGalerry,ProductSeries
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from checkout.models import Order
# Create your views here.
def store(request,category_slug=None):
    products=Product.objects.all().order_by('-created_at')
    list_brand=Brand.objects.all().values_list('brand_name').distinct()
    if category_slug is not None:
        products=Product.objects.filter(Q(category__slug=category_slug,is_active=True)).order_by('-created_at')         
        list_brand=Brand.objects.filter(category__slug=category_slug).values_list('brand_name').distinct()
    filter_products= request.GET.get('brand')
    filter_pricce=request.GET.get('price')
    if filter_products:
        products=Product.objects.filter(category__slug=category_slug,brand__brand_name__in=filter_products.split(','),is_active=True).order_by('-created_at')
  
    if filter_pricce:
        if filter_pricce=='lowprice':
            products=products.order_by('price')
        elif filter_pricce=='highprice':
            products=products.order_by('-price')
        elif filter_pricce=='bestsell':
            products=products.order_by('-sold')
   
 
    product_count=products.count()
    paginator = Paginator(products, 8) 
    page_number = request.GET.get('page')
    page_product = paginator.get_page(page_number)
    
    context={
        'products':page_product,
        'list_brand':list_brand,
        'product_count':product_count,
       
    }
    
    return render(request,'store/store.html',context)
def search(request):
    keyword=None
    products=Product.objects.all().order_by('-created_at')
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        products=Product.objects.filter(Q(category__slug__icontains=keyword)|Q(product_name__icontains=keyword)|Q(description__icontains=keyword))
    list_brand=Brand.objects.all().values_list('brand_name').distinct()

    filter_products= request.GET.get('brand')
    if filter_products:
        products=Product.objects.filter(brand__brand_name__in=filter_products.split(','),is_active=True).order_by('-created_at')
    
    filter_pricce=request.GET.get('price')
    if filter_pricce:
      
        if filter_pricce=='lowprice':
            products=products.order_by('price')
        elif filter_pricce=='highprice':
            products=products.order_by('-price')
        elif filter_pricce=='bestsell':
            products=products.order_by('-sold')
    product_count=products.count()
    paginator = Paginator(products, 8) 
    page_number = request.GET.get('page')
    page_product = paginator.get_page(page_number)
  
    context={
        'products':page_product,
        'product_count':product_count,
        'list_brand':list_brand,
        'keyword':keyword,
     
        
    }
    return render(request,'store/store.html',context)

def product_detail(request,category_slug,product_slug):
    product=Product.objects.get(category__slug=category_slug,slug=product_slug,is_active=True)
    try:
        product_series=Product.objects.filter(product_series_id=product.product_series.id)
    except:
        product_series=None
    reviewratings=ReviewRating.objects.filter(product_id=product.id)
    product_galleries=ProductGalerry.objects.filter(product_id=product.id)
    product_recommend=Product.objects.filter(brand__brand_name=product.brand.brand_name)[:8]

    if request.user.is_authenticated:
        order=Order.objects.filter(user=request.user,product__slug=product_slug,is_ordered=True)
        if len(order) == 0:
            order=None
    else:
        order=None

    list_rate=[]
    for i in range(5):#count from  1*->5*
        list_rate.append(ReviewRating.objects.filter(product_id=product.id,rating=i+1).count())
   
    context={
        'product':product,
        'reviewratings':reviewratings,
        'list_rate':list_rate,
        'order':order,
        'product_galleries':product_galleries,
        'product_recommend':product_recommend,
        'product_series':product_series

    }
    return render(request,'store/product_detail.html',context)

def reviewrating(request,product_id):
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        try:
            reviewrating=ReviewRating.objects.get(user_id=request.user.id,product_id=product_id)
           
            forms=ReviewForm(request.POST,instance=reviewrating)
            if forms.is_valid():
                forms.save()
                messages.success(request,'Cập nhật thành công')
                return redirect(url)
        except ReviewRating.DoesNotExist:
            forms=ReviewForm(request.POST)
            if forms.is_valid():
                reviewrating=ReviewRating()
                reviewrating.rating=forms.cleaned_data['rating']
                reviewrating.title=forms.cleaned_data['title']
                reviewrating.description=forms.cleaned_data['description']
                reviewrating.user_id=request.user.id
                reviewrating.product_id=product_id
                reviewrating.save()
                messages.success(request,'Đánh giá thành công')
                return redirect(url)


