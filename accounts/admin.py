from django.contrib import admin
from .models import Account,AccountProfile
# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display=['email','username','first_name','last_name','phone','is_active','is_staff','is_seller','is_admin','date_joined']
    search_fields=['email','username','phone']

class AccountProfileAdmin(admin.ModelAdmin):
    list_display=['user','address','birthday']

admin.site.register(Account,AccountAdmin)
admin.site.register(AccountProfile,AccountProfileAdmin)