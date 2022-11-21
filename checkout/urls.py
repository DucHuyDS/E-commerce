from django.urls import path
from . import views

urlpatterns = [
    path('',views.checkout,name='checkout'),
    path('payment/',views.payment,name='payment'),
    path('order_complete/',views.order_complete,name='order_complete'),

    
]
