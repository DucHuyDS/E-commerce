from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='log_out'),
    path('register/',views.register,name='register'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password/',views.reset_password,name='reset_password'),

    path('verify_email/',views.verify_email,name='verify_email'), 
    path('resend_verify_email/',views.resend_verify_email,name='resend_verify_email'),

    path('profile/',views.profile,name='profile'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('my_order/',views.my_order,name='my_order'),
    path('order_details/<str:payment_id>/',views.order_details,name='order_details'),  
    path('change_password/',views.change_password,name='change_password'),
]
