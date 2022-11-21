from django.db import models
from accounts.models import Account
from store.models import Product,Variation

# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.email

class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation)
    quantity=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)

    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.product.product_name
    
    def sub_total(self):
        return self.product.price*self.quantity