from django.urls import path
from . import views

urlpatterns = [
   path('',views.store,name='store'),
   path('search/',views.search,name='search'),
   path('<slug:category_slug>/',views.store,name='category_slug'),
   path('rating/<int:product_id>/',views.reviewrating,name='reviewrating'),
   
   # path('<slug:category_slug>/',views.search,name='search_category'),
   path('<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
   

]
