from django.urls import path 
from .views import *

app_name = "Nest"

urlpatterns = [
    path("home",index,name="index"),
    path('', Show_product_N, name='show_product'),
    path('view_product/<int:id>', View_product_N, name='view_product'),
    path('categories_product/', categories_product_N, name='categories_product'),
    path('search_category/<int:id>', search_category_N, name='search_category'),
    path('contact/',contact_N,name="contact"),
    path('about-us/', about_us_N, name='about_us'),
    path('Newsletter/', Newsletter_N, name='Newsletter'),
    path('search', search_item_N, name='search'),
    path('cart/', cart_N, name='cart'),
    
]

