from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('add_cart/<int:product_id>/<str:buynow>/',views.add_cart,name='add_cart'),

    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/',views.remove_cart_item,name='remove_cart_item'),
    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',views.delete_cart_item,name='delete_cart_item'),
 
    path('active_cart_item/<int:cart_item_id>/',views.active_cart_item,name='active_cart_item'),
    path('inactive_cart_item/<int:cart_item_id>/',views.inactive_cart_item,name='inactive_cart_item')

]
