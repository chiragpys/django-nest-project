from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

Gender_Choice = (
    ('Male','Male'),
    ('Female','Female'),
)

class State_name(models.Model):
    state = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.state)


class Product_categories(models.Model):
    categories = models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.categories)


class vendor_register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return str(self.user)
    


class Vendor_profile(models.Model):
    user = models.OneToOneField(vendor_register, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to="admin_profile/",null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(default=18, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender_Choice, default='Male')
    phone = models.IntegerField(null=True, blank=True)
    c_name = models.CharField(max_length=100, null=True, blank=True)
    c_email = models.EmailField(null=True, blank=True)
    c_website = models.URLField(null=True, blank=True)
    c_des = models.TextField(null=True, blank=True) 
    address = models.TextField(null=True, blank=True)
    location = models.ForeignKey(State_name, on_delete=models.CASCADE, null=True, blank=True)
    
    
    def __str__(self):
        return str(self.user)
 
 
@receiver(post_save, sender = vendor_register)
def create_Vendor_profile(sender, instance, created, **kwargs):
    if created:
        Vendor_profile.objects.create(user=instance)

@receiver(post_save, sender = vendor_register)
def save_user_Vendor_profile(sender, instance, **kwargs):
    instance.vendor_profile.save() 
 
   


class Upload_product(models.Model):
    user = models.ForeignKey(vendor_register, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.FloatField()
    old_price = models.FloatField()
    categories = models.ForeignKey(Product_categories, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    product_photo = models.ImageField(upload_to='Product_upload',blank=False)
    stock = models.IntegerField()
    description = models.CharField(max_length=1000)
    
    
    def __str__(self):
        return self.product_name


