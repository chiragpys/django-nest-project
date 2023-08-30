from django.db import models

# Create your models here.

class Subscribe(models.Model):
    email = models.EmailField()
    
    def __str__(self):
        return str(self.email)
    
class Contact(models.Model):
    First_name = models.CharField(max_length=100)
    Phone = models.IntegerField()
    subject = models.CharField(max_length=250)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return str(self.First_name)
    

    
    

