from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import *
from .forms import *
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import check_password
import random
from Vendor.models  import *
from django.db.models import Q
from Nest.views import *

# Create your views here.



def User_signup(request):
    if request.session.get('user_admin') != None:
        return redirect('User:show_product') 
    if request.method == "POST":
        lof = Signup_form(request.POST)
        if lof.is_valid():
            # email verification 
            user_email = lof.cleaned_data['email']
            if User.objects.filter(email__iexact = user_email).exists():
                messages.error(request,'emailid is already register ')
                return redirect('User:signup')
            else:
                lof.save()
                user = User.objects.get(username = lof.cleaned_data['username'])
                temp = user_register(user=user)
                temp.save()
                user.is_active = False
                user.save()
                messages.success(request,'Signup Successfully.!')
                
                #sending verfication mail
                subject = 'Account Verification Mail'
                message = f'Hello {user.username},\nEmail : {user.email}\nPlease verify your email id.. http://127.0.0.1:8000/user/email_verification/'
                email_from = settings.EMAIL_HOST_USER
                email_to = [user.email,]
                send_mail(subject, message, email_from, email_to)
                return redirect('User:Email_send')
        else:
            messages.error(request,'Something went wrong..!!')
    else:
        lof = Signup_form()
    tempalate = "User/signup.html"
    return render(request,tempalate,{'form':lof})


# This is a Show email Function.
def User_Email_send(request):
    return render(request,"User/email_sent.html")


# This is Function Email Verification.
def User_Email_verification(request):
    if request.session.get('user_admin') == None:
        if request.method == "POST":
            uev = Verification_Email_Form(request.POST)
            if uev.is_valid():
                form_email = uev.cleaned_data['email']
                try:
                    user_by_email = User.objects.get(email__iexact = form_email)
                    if user_by_email.is_active:
                        messages.error(request,'User is already verified, Please login..!')
                        return redirect('User:login')
                    else:
                        user_by_email.is_active = True
                        messages.success(request,'User Verification succesfull. Please login!')
                        user_by_email.save()
                        return redirect('User:login')
                except:
                    messages.error(request,"User not found with this email address,Please try again or signup!")
                    return redirect('User:Email_verification')
            else:
                messages.error(request,"Something went wrong..!!")
        else:
            uev = Verification_Email_Form()
    else:
        return redirect('User:login')
    
    tempalate = "User/email_verification.html"
    return render(request,tempalate,{'form':uev})

# This is a function is User Login for used
def User_login(request):
    if request.session.get('user_admin') == None:
        if request.method == "POST":
            ulf = Login_form(request=request, data = request.POST)
            if ulf.is_valid():
                username = ulf.cleaned_data['username']
                password = ulf.cleaned_data['password']
    
                # if  vendor_register.objects.filter(user__iexact = username).exists():
                #     messages.error(request,'This is a Vendor you can not login..!')
                #     return redirect('User:login')
                # else:
                # Authenticate method used
                user = authenticate(username=username,password=password)
                if user is not None:
                    user = User.objects.get(username = user)
                    if user.is_active == True:
                        user_admin = {
                            'username' : user.username,
                            'email' : user.email,
                        }
                        request.session['user_admin'] = user_admin
                        request.session['user_admin_email'] = user.email
                        if request.session.get('user_admin') != None:
                            messages.success(request,'Login Successfully.!')
                            return redirect('User:show_product') 
                        else:
                            return redirect('User:login')
                    else:
                        user.delete()
                        messages.error(request,'User Not found or Authenticated,please signup again!')
                        return redirect('User:signup')
                    
                else:
                    messages.error(request,'Provided ID and Password is wrong!')
            else:
                messages.error(request,'Something went wrong!!')
            
        else:
            ulf = Login_form()
    else:
        return redirect('User:profile')
    tempalate = "User/login.html"
    return render(request,tempalate,{'form':ulf})



# This is a function is User Logout for used
def User_logout(request):
    if request.session.get('user_admin') == None:
        return redirect('User:login')
    else:
        request.session.delete()
        return redirect('User:login')


# This is a function is User Set Password Change for used
def User_Set_password(request):
    if request.session.get('user_admin') != None:
        c = Cart.objects.count()
        user_data = User.objects.get(username=request.session.get('user_admin')['username'])
        user = User.objects.get(email__iexact = request.session.get('user_admin_email'))
        if request.method == "POST":
            upc = Pass_Change(user, data=request.POST)
            if upc.is_valid():
                upc.save()
                messages.success(request,'Password changed successfuly..!')
                return redirect('User:profile')
            else:
                messages.error(request,'Something went wrong')            
        else:
            upc = Pass_Change(user)
        tempalate = "User/password-set.html"
        return render(request, tempalate,{'form':upc,'u_name':user_data,'c':c})
    else:
        return redirect('User:login')



# This is a function is User Password Forgot for used    
def User_forgot_password(requset):
    if requset.session.get('user_admin') == None:
        if requset.method == "POST":
            ufp = Forgot_password_from(requset.POST)
            if ufp.is_valid():
                email = ufp.cleaned_data['email']
                if User.objects.filter(email__iexact = email).exists():
                    OTP = random.randint(111111,999999)
                    subject = 'Password Reset OTP'
                    message = f"Your OTP is, {OTP} \nPlease Follow This Link to verify OTP, --> http://127.0.0.1:8000/"
                    email_from = settings.EMAIL_HOST_USER
                    email_to = [email, ]
                    send_mail(subject, message, email_from, email_to)
                    requset.session['user_sent_otp'] = OTP
                    requset.session['user_forgot_pw_email'] = email
                    requset.session.set_expiry(900)
                    return redirect('User:verify_otp') 
                else:
                    messages.error(requset,'User with this email not found!')
                    return redirect('User:forgot_password')
            else:
                messages.error(requset,'Something went wrong..!')
                return redirect('User:forgot_password')
        else:
            ufp = Forgot_password_from()
        tempalte = "User/forgot_password.html"
        return render(requset,tempalte,{'form':ufp})
    else:
        return redirect("User:profile")



# This is a function Forgot password OTP Verification can used
def User_verify_otp(request):
    if request.session.get('user_forgot_pw_email') != None:
        if request.method == "POST":
            uvo = verify_otp_form(request.POST)
            if uvo.is_valid():
                otp = uvo.cleaned_data['otp']
                if otp == request.session.get('user_sent_otp'):
                    return redirect("User:reset_password")
                else:
                    messages.error(request,"OTP does not match. Try again")
                    return redirect("User:verify_otp")
            else:
                messages.error(request,"Something went wrong..!!")
                return redirect("User:verify_otp")
        else:
            uvo = verify_otp_form()
        template = "User/forgot_password.html"
        return render (request,template,{'otp':uvo})
    else:
        return redirect("User:forgot_password")



# This is a function Reset Password can used
def User_reset_password(request):
    if request.session.get('user_forgot_pw_email') != None:
        user = User.objects.get(email__iexact = request.session.get('user_forgot_pw_email'))
        if request.method == "POST":
            urp = Set_Change(user,request.POST)
            if urp.is_valid():
                urp.save()
                messages.success(request, 'Password has been changed successfully..!')
                return redirect('User:login')
            else:
                messages.error(request,'New and confirm password are not same !')
        else:
            urp = Set_Change(user)
        tempalte = "User/password-reset.html"
        return render(request, tempalte,{'form':urp})

    else:
        return redirect("User:forgot_password")


# This is a Function User Profile can used 
def User_profile_fun(request):
    if request.session.get('user_admin') != None:
        if not User.objects.filter(username=request.session.get('user_admin')['username']).exists():
            messages.error(request,'User not found! Please signup!')
            request.session.delete()
            return redirect('User:signup')
        user_data = User.objects.get(username=request.session.get('user_admin')['username'])
        c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
        if request.method == "POST":
            user_form = User_form(request.POST, instance=user_data)
            user_profile_form = User_profile_form(request.POST, request.FILES, instance=user_data.user_register.user_profile)
            if user_form.is_valid() and user_profile_form.is_valid():
                user_form.save()
                user_profile_form.save()
                messages.success(request,"Data Saved Successfully.!")
            else:
                messages.error(request,"Something went wrong..!")
                return redirect('User:profile')
        else:
            user_form = User_form(instance=user_data)
            user_profile_form = User_profile_form(instance=user_data.user_register.user_profile)
        image_user = user_profile.objects.get(user = user_data.user_register)
        if user_profile.objects.filter(image=image_user.image).exists():
            img = image_user.image
        else:
            pass
        context = {
            'user_form' : user_form,
            'profile_form' : user_profile_form,
            'img' : img,
            'name' : user_data,
            'u_name' : user_data,
            'c':c
        }
        tempalate = "User/profile.html"
        return render(request,tempalate,context)
    else:
        return redirect('User:login')


   
# This is a function Show the all Product in home page
def Show_product(request):
    if request.session.get('user_admin') != None:
        user_data = User.objects.get(username=request.session.get('user_admin')['username'])
        data = Upload_product.objects.all()
        name = Vendor_profile.objects.all()
        c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
        context = {
            'form':data,
            'name':name,
            'c':c,
            'u_name' : user_data
        }
        tempalate = "User/show/Show.html"
        return render(request,tempalate,context)
    else:
        return redirect('User:login')


# This is a function Only one Product details viewd  
def View_product(request,id):
    user_data = User.objects.get(username=request.session.get('user_admin')['username'])
    c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
    if request.session.get('user_admin') != None:
        data = Upload_product.objects.get(pk=id)
        name = Vendor_profile.objects.get(user=data.user)
        tempalate = "User/show/view.html"
        return render(request,tempalate,{'form':data,'name':name,'u_name':user_data,'c':c})
    else:
        return redirect('User:login')
    


# This is a function Show the all Product category
def categories_product(request):
    user_data = User.objects.get(username=request.session.get('user_admin')['username'])
    c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
    if request.session.get('user_admin') != None:
        categories_product = Product_categories.objects.all()
        tempalate = "User/show/categories.html"
        return render(request,tempalate,{'category':categories_product,'u_name':user_data,'c':c})
    else:
        return redirect('User:login')


   
# This is a function search category of Products 
def search_category(request,id):
    user_data = User.objects.get(username=request.session.get('user_admin')['username'])
    c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
    if request.session.get('user_admin') != None:
        categories_product = Product_categories.objects.all()
        categories = Product_categories.objects.get(pk=id)
        product_cat = Upload_product.objects.filter(categories=categories)
        tempalate = "User/show/categories.html"
        return render(request,tempalate,{'category':categories_product,'view_product':product_cat,'u_name':user_data,'c':c})
    else:
        return redirect('User:login')
    
    
 # Search Item all page   
def search_item(request):
    user_data = User.objects.get(username=request.session.get('user_admin')['username'])
    c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
    if request.session.get('user_admin') != None:
        query = request.GET.get('q')
        categories_product = Product_categories.objects.all()
        if query:
            product_cat = Upload_product.objects.filter(
                Q(product_name__icontains=query)
            )
        else:
            product_cat = Upload_product.objects.all()
        return render(request, "User/show/categories.html", {'category':categories_product,'view_product': product_cat,'u_name':user_data,'c':c})
    else:
        return redirect('User:login')


# Add to cart
def Add_to_cart(request,id):
    if request.session.get('user_admin') != None:
        user_data = User.objects.get(username=request.session.get('user_admin')['username'])
        data = Upload_product.objects.get(pk=id)
        cart = Cart.objects.create(user=user_data.user_register.user_profile, product=data)
        cart.save()
        return redirect('User:show_product')
    else:
        return redirect('User:login')
    
# Cart view  
def Cart_view(request):
    if request.session.get('user_admin') != None:
        user_data = User.objects.get(username=request.session.get('user_admin')['username'])
        cart = Cart.objects.filter(user=user_data.user_register.user_profile)
        c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
        template = "User/cart.html"
        return render(request,template,{'cart':cart,'c':c,'u_name':user_data})
    else:
        return redirect('User:login')

# Cart item remove 
def Cart_remove(request,id):
    if request.session.get('user_admin') != None:
        cart = Cart.objects.get(pk=id)
        cart.delete()
        return redirect('User:Cart_view') 
    else:
        return redirect('User:login')


# Newsletter
def Newsletter(request):
    if request.method == "GET":
        email = request.GET.get('email')
        print(email)
        nl = Subscribe(email=email)
        nl.save()
        
        # sned message 
        # subject = f'Subscription Of Nest'
        # message = f'Thank You for Subscribing with us you will get every update from us.\nYou can know about us more in: http://127.0.0.1:8000'
        # email_from = settings.EMAIL_HOST_USER
        # email_to = [email, ]
        # send_mail(subject, message, email_from, email_to)
        
        return redirect("User:show_product")
    template = "common_user.html"
    return render(request,template)


# Contact page
def contact(request):
    user_data = User.objects.get(username=request.session.get('user_admin')['username'])
    c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
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
    template="User/contact.html"
    return render(request,template,{'form': form,'u_name':user_data,'c':c}) 


# About-up page
def about_us(request):
    user_data = User.objects.get(username=request.session.get('user_admin')['username'])
    c = Cart.objects.filter(user=user_data.user_register.user_profile).count()
    template="User/about-us.html"
    return render(request,template,{'u_name':user_data,'c':c})  

