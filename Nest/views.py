from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from Vendor.models import *
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


def index(request):
    template="index.html"
    return render(request,template)



def contact_N(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['First_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            # phone = form.changed_data['Phone']
            subject = f'Thank You {name} for Approaching Us'
            message = f'Hello {name},' + "\nEmail : " + email +  f"\nHere is your requested message: {message}"
            email_from = settings.EMAIL_HOST_USER
            email_to = [email, ]
            send_mail(subject, message, email_from, email_to)
            form.save()
            return redirect("User:show_product")
    else:
        form = ContactForm()
    template="contact.html"
    return render(request,template,{'form': form})


def Newsletter_N(request):
    if request.method == "GET":
        email = request.GET.get('email')
        print(email)
        nl = Subscribe(email=email)
        nl.save()
        # sned message 
        subject = f'Subscription Of Nest'
        message = f'Thank You for Subscribing with us you will get every update from us.\nYou can know about us more in: http://127.0.0.1:8000'
        email_from = settings.EMAIL_HOST_USER
        email_to = [email,]
        send_mail(subject, message, email_from, email_to)
        
        return redirect("Nest:show_product")
    template = "common.html"
    return render(request,template)


def about_us_N(request):
    template="about-us.html"
    return render(request,template)



# This is a function Show the all Product in home page
def Show_product_N(request):
        data = Upload_product.objects.all()
        name = Vendor_profile.objects.all()
        tempalate = "Show.html"
        return render(request,tempalate,{'form':data,'name':name})


# This is a function Only one Product details viewd  
def View_product_N(request,id):
        data = Upload_product.objects.get(pk=id)
        name = Vendor_profile.objects.get(user=data.user)
        tempalate = "view.html"
        return render(request,tempalate,{'form':data,'name':name})

    


# This is a function Show the all Product category
def categories_product_N(request):
        categories_product = Product_categories.objects.all()
        tempalate = "categories.html"
        return render(request,tempalate,{'category':categories_product})



   
# This is a function search category of Products 
def search_category_N(request,id):
        categories_product = Product_categories.objects.all()
        categories = Product_categories.objects.get(pk=id)
        product_cat = Upload_product.objects.filter(categories=categories)
        tempalate = "categories.html"
        return render(request,tempalate,{'category':categories_product,'view_product':product_cat})


# Search items all 
def search_item_N(request):
    query = request.GET.get('q')
    categories_product = Product_categories.objects.all()
    if query:
        product_cat = Upload_product.objects.filter(
            Q(product_name__icontains=query)
         )
    else:
        product_cat = Upload_product.objects.all()
    return render(request, "categories.html",{'category':categories_product,'view_product': product_cat})

def cart_N(request):
    return render(request,'cart.html')

