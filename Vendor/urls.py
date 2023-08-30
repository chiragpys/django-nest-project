from django.urls import path
from .views import *
from Nest.views import *
app_name = "vendor"

urlpatterns = [
    path('',Vendor_signup, name="signup"),
    path('email_send/',Vendor_Email_send, name='Email_send'),
    path('email_verification/',Vendor_Email_verification,name='Email_verification'),
    path('login/',Vendor_login, name='login'),
    path('profile/',Vendor_profile_fun, name='profile'),
    path('logout/',Vendor_logout, name='logout'),
    path('set_password/',Vendor_Set_password, name='Set_password'),
    path('forgot_password/',Vendor_forgot_password, name='forgot_password'),
    path('verify_otp/',Vendor_verify_otp, name='verify_otp'),
    path('reset_password/',Vendor_reset_password, name='reset_password'),
    path('product_upload/', Product_upload, name='product_upload'),
    path('show_product/',Show_product, name='show_product'),
    path('product_update/<int:id>', Product_update, name='product_update'),
    path('product_delete/<int:id>', Product_delete, name='product_delete'),
    path('view_product/<int:id>', View_product, name='view_product'),
    path('Newsletter_vendor/', Newsletter_vendor, name='Newsletter_vendor'),
    
    
]
