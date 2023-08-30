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
from Nest.models import *


# Create your views here.


# Vendor Signup
def Vendor_signup(request):
    if request.session.get('vendor_admin') == None:
        if request.method == "POST":
            lof = Signup_form(request.POST)
            if lof.is_valid():
                # email verification 
                user_email = lof.cleaned_data['email']
                if User.objects.filter(email__iexact = user_email).exists():
                    messages.error(request,'emailid is already register ')
                    return redirect('vendor:signup')
                else:
                    lof.save()
                    user = User.objects.get(username = lof.cleaned_data['username'])
                    temp = vendor_register(user=user)
                    temp.save()
                    user.is_active = False
                    user.save()
                    messages.success(request,'Signup Successfully.!')
                    
                    #sending verfication mail
                    subject = 'Account Verification Mail'
                    message = f'Hello {user.username},\nEmail : {user.email}\nPlease verify your email id.. http://127.0.0.1:8000/vendor/email_verification/'
                    email_from = settings.EMAIL_HOST_USER
                    email_to = [user.email,]
                    send_mail(subject, message, email_from, email_to)
                    return redirect('vendor:Email_send')
            else:
                messages.error(request,'Something went wrong..!!')
        else:
            lof = Signup_form()
        tempalate = "vendor/signup.html"
        return render(request,tempalate,{'form':lof})
    else:
        return redirect('vendor:show_product')
        


# This is a Show email Function.
def Vendor_Email_send(request):
    return render(request,"vendor/email_sent.html")


# This is Function Email Verification.
def Vendor_Email_verification(request):
    if request.session.get('vendor_admin') == None:
        if request.method == "POST":
            vev = Verification_Email_Form(request.POST)
            if vev.is_valid():
                form_email = vev.cleaned_data['email']
                try:
                    user_by_email = User.objects.get(email__iexact = form_email)
                    if user_by_email.is_active:
                        messages.error(request,'User is already verified, Please login..!')
                        return redirect('vendor:login')
                    else:
                        user_by_email.is_active = True
                        user_by_email.is_staff = True
                        messages.success(request,'User Verification succesfull. Please login!')
                        user_by_email.save()
                        return redirect('vendor:login')
                except:
                    messages.error(request,"User not found with this email address,Please try again or signup!")
                    return redirect('vendor:Email_verification')
            else:
                messages.error(request,"Something went wrong..!!")
        else:
            vev = Verification_Email_Form()
    else:
        return redirect('vendor:login')
    
    tempalate = "vendor/email_verification.html"
    return render(request,tempalate,{'form':vev})


# Vendoe Login
def Vendor_login(request):
    if request.session.get('vendor_admin') == None:
        if request.method == "POST":
            vlf = Login_form(request=request, data = request.POST)
            if vlf.is_valid():
                username = vlf.cleaned_data['username']
                password = vlf.cleaned_data['password']
                # Authenticate method used
                user = authenticate(username=username,password=password)
                if user is not None:
                    user = User.objects.get(username = user)
                    if user.is_active == True:
                        vendor_admin = {
                            'username' : user.username,
                            'email' : user.email,
                        }
                        request.session['vendor_admin'] = vendor_admin
                        request.session['vendor_admin_email'] = user.email
                        if request.session.get('vendor_admin') != None:
                            return redirect('vendor:profile') 
                        else:
                            return redirect('vendor:login')
                    else:
                        user.delete()
                        messages.error(request,'User Not found or Authenticated,please signup again!')
                        return redirect('vendor:signup')
                    
                else:
                    messages.error(request,'Provided ID and Password is wrong!')
            else:
                messages.error(request,'Something went wrong!!')
            messages.success(request,'Login Successfully.!')
        else:
            vlf = Login_form()
    else:
        return redirect('vendor:profile')
    tempalate = "vendor/login.html"
    return render(request,tempalate,{'form':vlf})



# Vendor Logout
def Vendor_logout(request):
    if request.session.get('vendor_admin') == None:
        return redirect('vendor:login')
    else:
        request.session.delete()
        return redirect('vendor:login')


# Vendor Set-Password
def Vendor_Set_password(request):
    if request.session.get('vendor_admin') != None:
        user_data = User.objects.get(username=request.session.get('vendor_admin')['username'])
        user = User.objects.get(email__iexact = request.session.get('vendor_admin_email'))
        if request.method == "POST":
            vpc = Pass_Change(user, data=request.POST)
            if vpc.is_valid():
                vpc.save()
                messages.success(request,'Password changed successfuly..!')
                return redirect('vendor:profile')
            else:
                messages.error(request,'Something went wrong')            
        else:
            vpc = Pass_Change(user)
        tempalate = "vendor/password-set.html"
        return render(request, tempalate,{'form':vpc,'v_name':user_data})
    else:
        return redirect('vendor:login')



# Vendor Forgot-Password
def Vendor_forgot_password(requset):
    if requset.session.get('vendor_admin') == None:
        if requset.method == "POST":
            vfp = Forgot_password_from(requset.POST)
            if vfp.is_valid():
                email = vfp.cleaned_data['email']
                if User.objects.filter(email__iexact = email).exists():
                    OTP = random.randint(111111,999999)
                    subject = 'Password Reset OTP'
                    message = f"Your OTP is, {OTP} \nPlease Follow This Link to verify OTP, --> http://127.0.0.1:8000/"
                    email_from = settings.EMAIL_HOST_USER
                    email_to = [email, ]
                    send_mail(subject, message, email_from, email_to)
                    requset.session['vendor_sent_otp'] = OTP
                    requset.session['vendor_forgot_pw_email'] = email
                    requset.session.set_expiry(900)
                    return redirect('vendor:verify_otp') 
                else:
                    messages.error(requset,'User with this email not found!')
                    return redirect('vendor:forgot_password')
            else:
                messages.error(requset,'Something went wrong..!')
                return redirect('vendor:forgot_password')
        else:
            vfp = Forgot_password_from()
        tempalte = "vendor/forgot_password.html"
        return render(requset,tempalte,{'form':vfp})
    else:
        return redirect("vendor:profile")

    
# Vendor OTP verification
def Vendor_verify_otp(request):
    if request.session.get('vendor_forgot_pw_email') != None:
        if request.method == "POST":
            vvo = verify_otp_form(request.POST)
            if vvo.is_valid():
                otp = vvo.cleaned_data['otp']
                if otp == request.session.get('vendor_sent_otp'):
                    return redirect("vendor:reset_password")
                else:
                    messages.error(request,"OTP does not match. Try again")
                    return redirect("vendor:verify_otp")
            else:
                messages.error(request,"Something went wrong..!!")
                return redirect("vendor:verify_otp")
        else:
            vvo = verify_otp_form()
        template = "vendor/forgot_password.html"
        return render (request,template,{'otp':vvo})
    else:
        return redirect("vendor:forgot_password")
 
 
# Vendor Password Reset  
def Vendor_reset_password(request):
    if request.session.get('vendor_forgot_pw_email') != None:
        user = User.objects.get(email__iexact = request.session.get('vendor_forgot_pw_email'))
        if request.method == "POST":
            vrp = Set_Change(user,request.POST)
            if vrp.is_valid():
                vrp.save()
                messages.success(request, 'Password has been changed successfully..!')
                return redirect('vendor:login')
            else:
                messages.error(request,'New and confirm password are not same !')
        else:
            vrp = Set_Change(user)
        tempalte = "vendor/password-reset.html"
        return render(request, tempalte,{'form':vrp})

    else:
        return redirect("vendor:forgot_password") 


# Vendor Profile
def Vendor_profile_fun(request):
    if request.session.get('vendor_admin') != None:
        if not User.objects.filter(username=request.session.get('vendor_admin')['username']).exists():
            messages.error(request,'User not found! Please signup!')
            request.session.delete()
            return redirect('vendor:signup')
        user_data = User.objects.get(username=request.session.get('vendor_admin')['username'])
        if request.method == "POST":
            vendor_user_form = User_form(request.POST, instance=user_data)
            vendor_profile_form = Admin_profile_form(request.POST, request.FILES, instance=user_data.vendor_register.vendor_profile)
            if vendor_user_form.is_valid() and vendor_profile_form.is_valid():
                vendor_user_form.save()
                vendor_profile_form.save()
                messages.success(request,"Data Saved Successfully.!")
            else:
                messages.error(request,"Something went wrong..!")
                return redirect('vendor:profile')
        else:
            vendor_user_form = User_form(instance=user_data)
            vendor_profile_form = Admin_profile_form(instance=user_data.vendor_register.vendor_profile)
        image_user = Vendor_profile.objects.get(user = user_data.vendor_register)
        if Vendor_profile.objects.filter(image=image_user.image).exists():
            img = image_user.image
        else:
            pass
        context = {
            'user_form' : vendor_user_form,
            'profile_form' : vendor_profile_form,
            'img' : img,
            'v_name':user_data,
        }
        tempalate = "vendor/profile.html"
        return render(request,tempalate,context)
    else:
        return redirect('vendor:login')


# Vendor Product Upload
def Product_upload(request):
    if request.session.get('vendor_admin') != None:
        user_data = User.objects.get(username=request.session.get('vendor_admin')['username'])
        if request.method == "POST":
            vpu = Product_from(request.POST, request.FILES)
            if vpu.is_valid():
                temp = vpu.save(commit=False)
                temp.user = user_data.vendor_register
                temp.save()
                messages.success(request,"Product Upload Successfully..")
                return redirect('vendor:show_product')
            else:
                messages.error(request,'Somethink went worng....')
                print("no")
        else:
            vpu = Product_from()
        tempalate = "vendor/product-upload.html"
        return render(request,tempalate,{'form':vpu,'v_name':user_data})
    else:
        return redirect('vendor:login')


# Vendor Show all Product 
def Show_product(request):
    if request.session.get('vendor_admin') != None:
        user_data = User.objects.get(username=request.session.get('vendor_admin')['username'])
        data = Upload_product.objects.filter(user=user_data.vendor_register)
        name = Vendor_profile.objects.filter(user=user_data.vendor_register)
        tempalate = "vendor/Show.html"
        return render(request,tempalate,{'form':data,'name':name,'v_name':user_data})
    else:
        return redirect('vendor:login')


# Vendor Product Update
def Product_update(request,id):
    if request.session.get('vendor_admin') != None:
        user_data = User.objects.get(username=request.session.get('vendor_admin')['username'])
        data = Upload_product.objects.get(pk=id) 
        if request.method == "POST":
            vpu = Product_from(request.POST, request.FILES, instance=data)
            if vpu.is_valid():
                temp = vpu.save(commit=False)
                temp.user = user_data.vendor_register
                temp.save()
                messages.success(request,"Product Upload Successfully..")
                return redirect('vendor:show_product')
            else:
                messages.error(request,'Somethink went worng....')
        else:
            vpu = Product_from(instance=data)
        tempalate = "vendor/product-update.html"
        return render(request,tempalate,{'form':vpu,'v_name':user_data})
    else:
        return redirect('vendor:login')


# Vendor Product Detele    
def Product_delete(request,id):
    if request.session.get('vendor_admin') != None:
        data = Upload_product.objects.get(pk=id)
        data.delete()
        return redirect('vendor:show_product') 
    else:
        return redirect('vendor:login')


# Vendor Product details shows   
def View_product(request,id):
    if request.session.get('vendor_admin') != None:
        user_data = User.objects.get(username=request.session.get('vendor_admin')['username'])
        data = Upload_product.objects.get(pk=id)
        name = Vendor_profile.objects.get(user=data.user)
        tempalate = "vendor/view.html"
        return render(request,tempalate,{'form':data,'name':name,'v_name':user_data})
    else:
        return redirect('vendor:login')

  
# Vendoe News-letters   
def Newsletter_vendor(request):
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
        return redirect("vendor:show_product")
    template = "common.html"
    return render(request,template)
