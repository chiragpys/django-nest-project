from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Vendor.models import *




# Create your models here.

Gender_Choice = (
    ('Male','Male'),
    ('Female','Female'),
)


class user_register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return str(self.user)
    

class user_profile(models.Model):
    user = models.OneToOneField(user_register, on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(upload_to="User_profile/",null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=Gender_Choice, default='Male')
    phone = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return str(self.user) 


@receiver(post_save, sender = user_register)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(user=instance)

@receiver(post_save, sender = user_register)
def save_user_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()  
    

class Cart(models.Model):
    user = models.ForeignKey(user_profile, on_delete=models.CASCADE)
    product = models.ForeignKey(Upload_product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=True, blank=True)
    cart_date = models.DateField(auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return str(self.product.product_name)
