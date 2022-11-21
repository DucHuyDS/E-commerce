from django.contrib import admin
from .models import Payment,Order,Contact,Discount
# Register your models here.
class PaymentAdmin(admin.ModelAdmin):
    list_display=['payment_id','status']

class OrderAdmin(admin.ModelAdmin):
    list_display=['user','payment']

class ContactAdmin(admin.ModelAdmin):
    list_display=['user','full_name','payment','phone','address']

admin.site.register(Order,OrderAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Contact,ContactAdmin)
admin.site.register(Discount)