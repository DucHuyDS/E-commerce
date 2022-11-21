from django.db import models
from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from accounts.models import Account
from django.db.models import Count,Avg
from ckeditor.fields import RichTextField
from django.utils.text import slugify
# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='category_name')
    img=models.FileField(upload_to='photos/category',validators=[FileExtensionValidator(['pdf','svg','jpg','png','jpeg',''])])

    def get_url(self):
        return reverse('category_slug',args=[self.slug])

    def __str__(self):
        return self.category_name

    def count_product(self):
        count=0
        products=Product.objects.filter(category=self,is_active=True).aggregate(count=Count('product_name'))
        if products['count']:
            count=products['count']
        return count

class Brand(models.Model):
    brand_name=models.CharField(max_length=100)
    slug=AutoSlugField(populate_from='brand_name')
    created_at=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.brand_name

    def get_url(self):
        return reverse('search_brand',args=[self.category.slug,self.slug])

    def count_product(self):
        count=0
        products=Product.objects.filter(brand=self,is_active=True).aggregate(count=Count('product_name'))
        if products['count']:
            count=products['count']
        return count

    
class ProductSeries(models.Model):
    series=models.CharField(max_length=100,unique=True)
    def __str__(self):
        return self.series



class Product(models.Model):
    product_series=models.ForeignKey(ProductSeries,on_delete=models.CASCADE,null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=200)
    config=models.CharField(max_length=100,default=None,blank=True,null=True)
    slug = AutoSlugField(populate_from='product_name')
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    description=models.TextField()
    img=models.ImageField(upload_to='photos/product')
    sold=models.IntegerField(default=0)
    price=models.IntegerField()
    stock=models.IntegerField()
    content=RichTextField()
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug= slugify(self.product_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_detail',args=[self.category.slug,self.slug])

    def average_rating(self,avg=0):
        rating=ReviewRating.objects.filter(product=self).aggregate(avg=Avg('rating'))
        if rating['avg']:
            return round(rating['avg'],1)
        return avg
       
    def count_rating(self):
        return ReviewRating.objects.filter(product=self).aggregate(count=Count('rating'))['count']



class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager,self).filter(variation_caterogy='màu',is_active=True)
    def sizes(self):
        return super(VariationManager,self).filter(variation_caterogy='cỡ',is_active=True)

variation_caterogy_choice=(
    ('màu','màu'),
    ('cỡ','cỡ'),
)

class Variation(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_caterogy=models.CharField(max_length=100,choices=variation_caterogy_choice)
    variation_value=models.CharField(max_length=100)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
    objects=VariationManager()
    def __str__(self):
        return self.variation_value


class ProductGalerry(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    img=models.ImageField(upload_to='photos/productgallery')
    

class ReviewRating(models.Model):
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title=models.CharField(max_length=100,blank=True)
    description=models.TextField(max_length=500,blank=True)
    rating=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.product


