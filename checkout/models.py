from venv import create
from django.db import models
from cart.models import CartItem
from accounts.models import Account
from store.models import Product,Variation

# Create your models here.
class Payment(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id=models.CharField(max_length=30)
    status=models.CharField(max_length=30)
    discount=models.FloatField(default=0)
    price=models.IntegerField(default=0)
    tax=models.FloatField(default=0)
    total_price=models.FloatField(default=0)
    created_at=models.DateTimeField()
    updated_at=models.DateTimeField()

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variations=models.ManyToManyField(Variation)
    quantity=models.IntegerField(default=0)
    sub_total=models.FloatField(default=0)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_ordered=models.BooleanField(default=False)
    
    def __str__(self):  
        return self.user.email
    
    

class Contact(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    phone=models.IntegerField(null=True)
    address=models.CharField(max_length=100,blank=True)
    full_name=models.CharField(max_length=100,blank=True)
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email

class Discount(models.Model):
    name=models.CharField(max_length=100)
    price=models.FloatField(default=0)
    create_at=models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.name