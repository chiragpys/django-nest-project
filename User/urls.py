from django.urls import path
from .views import *
from Nest.views import *
app_name = 'User'

urlpatterns = [
    path('signup/', User_signup, name='signup'),
    path('Email_send/', User_Email_send, name='Email_send'),
    path('email_verification/', User_Email_verification, name='Email_verification'),
    path('login/', User_login, name='login'),
    path('profile/', User_profile_fun, name='profile'),
    path('logout/', User_logout, name='logout'),
    path('Set_password/', User_Set_password, name='Set_password'),
    path('forgot_password/', User_forgot_password, name='forgot_password'),
    path('verify_otp/', User_verify_otp, name='verify_otp'),
    path('reset_password/', User_reset_password, name='reset_password'),
    path('', Show_product, name='show_product'),
    path('view_product/<int:id>', View_product, name='view_product'),
    path('categories_product/', categories_product, name='categories_product'),
    path('search_category/<int:id>', search_category, name='search_category'),
    path('search/', search_item, name='search'),
    path('contact/',contact,name="contact"),
    path('aboutus/', about_us, name='about_us'),
    path('Newsletter/', Newsletter, name='Newsletter'),
    path('Add_to_cart/<int:id>', Add_to_cart, name='Add_to_cart'),
    path('Cart_view/', Cart_view, name='Cart_view'),
    path('Cart_remove/<int:id>', Cart_remove, name='Cart_remove'),
   
]
