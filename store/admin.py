from django.contrib import admin
from .models import Product,Category,Variation,ReviewRating,Brand,ProductGalerry,ProductSeries
from django.utils.html import  format_html
import admin_thumbnails

# Register your models here.
@admin_thumbnails.thumbnail('img')
class ProductGalleryAdmin(admin.TabularInline):
    model=ProductGalerry
    extra=1

@admin_thumbnails.thumbnail('img')
class ProductAdmin(admin.TabularInline):
    model=Product
    extra=1

class BrandInline(admin.TabularInline):
    model=Brand
    extra=1

class VariationAdmin(admin.TabularInline):
    model=Variation
    extra=1



class ProductSeiesAdmin(admin.ModelAdmin):
    fields=['series']
    inlines=[ProductAdmin]

class CategoryAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html("<img src='{}' width='30px' border-radius:100% ;".format(object.img.url))
    thumbnail.description='img'
    list_display=['category_name','slug','thumbnail']
    inlines=[BrandInline]
    
class ProductAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html("<img src='{}' width:'10px' height='50px' border-radius:100% ".format(object.img.url))

    list_display=['product_name','slug','sold','thumbnail','is_active']
    inlines=[ProductGalleryAdmin,VariationAdmin]

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display=['user','product','rating','title']



admin.site.register(Category,CategoryAdmin)
admin.site.register(ProductSeries,ProductSeiesAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(ReviewRating,ReviewRatingAdmin)