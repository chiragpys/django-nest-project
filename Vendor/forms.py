from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.contrib.auth.models import User



# <=========== Vendor SignUp Forms =============>
class Signup_form(UserCreationForm):
    username = forms.CharField(required=True, max_length=150, label='Username *', label_suffix="", widget=forms.TextInput(attrs={
        'id':"id_username", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Username',
    }))
    email = forms.EmailField(required=True,max_length=254, label_suffix="", label='Email address', widget=forms.EmailInput(attrs={
        'id':"id_email", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Email Id',
    }))
    password1 = forms.CharField(required=True, min_length=8, label='Password *', label_suffix="", widget=forms.PasswordInput(attrs={
        'id':"id_password1", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Password',
    }))
    password2 = forms.CharField(required=True, min_length=8, label='Password Confirmation *', label_suffix="", widget=forms.PasswordInput(attrs={
        'id':"id_password2", 
        'class':"ctrlHolder",
        'placeholder': 'Confirm your Password',
    }))
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        # widgets = {
        #     'username' : forms.TextInput(attrs={
        #         'id':"id_username", 
        #         'class':"ctrlHolder",
        #         'placeholder': 'Enter your Username',
        #         'maxlength':"3",
        #     })
        # }
        


# <=========== Vendor Verificatio Email Forms =============>
class Verification_Email_Form(forms.ModelForm):
    email = forms.EmailField(required=True,max_length=254, label_suffix="", label='Email address *', widget=forms.EmailInput(attrs={
        'id':"id_email", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Verify Email Id',
    }))
    class Meta:
        model = User
        fields = ['email'] 


# <=========== Vendor Login  Forms =============>
class Login_form(AuthenticationForm):
    username = forms.CharField(required=True, max_length=150, label='Username *', label_suffix="", widget=forms.TextInput(attrs={
        'id':"id_username", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Username',
    }))
    password = forms.CharField(required=True, min_length=8, label='Password *', label_suffix="", widget=forms.PasswordInput(attrs={
        'id':"id_password", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Password',
    })) 
    class Meta:
        model = User
        fields = ['username']


# <=========== Vendor Set password Change Forms =============>
class Pass_Change(PasswordChangeForm):
        old_password = forms.CharField(required=True, label='Old Password', label_suffix="", widget=forms.PasswordInput(attrs={
                'id':"id_password_old", 
                'class':"ctrlHolder",
                'placeholder': 'Enter Your Old Password',
            }))
        new_password1 = forms.CharField(required=True, label='New Password', label_suffix="", widget=forms.PasswordInput(attrs={
                'id':"id_new_password1", 
                'class':"ctrlHolder",
                'placeholder': 'Enter New Password ',
            }))
        new_password2 = forms.CharField(required=True, label='Confirm Password', label_suffix="", widget=forms.PasswordInput(attrs={
                'id':"id_new_password2", 
                'class':"ctrlHolder",
                'placeholder': 'Enter Confirm Password ',
            }))
    
        class Meta:
            model = User


           
# <=========== Vendor Forgot password Forms =============>
class Forgot_password_from(forms.ModelForm):
    email = forms.EmailField(required=True, max_length=254, label_suffix="", label='Email address *', widget=forms.EmailInput(attrs={
        'id':"id_email", 
        'class':"ctrlHolder",
        'placeholder': 'Enter your Email Id',
    }))
    class Meta:
        model = User
        fields = ['email']



# <=========== Vendor OTP verification Forms =============>       
class verify_otp_form(forms.Form):
    otp = forms.IntegerField(required=True,label_suffix="", label='OTP *', widget=forms.NumberInput(attrs={ 
        'class':"ctrlHolder",
        'placeholder': 'Enter OTP',
    }))       


# <=========== Vendor Forgot Password Forms =============>
class Set_Change(SetPasswordForm):
        new_password1 = forms.CharField(required=True, label='New Password', label_suffix="", widget=forms.PasswordInput(attrs={
                'id':"id_new_password1", 
                'class':"ctrlHolder",
                'placeholder': 'Enter New Password ',
            }))
        new_password2 = forms.CharField(required=True, label='Confirm Password', label_suffix="", widget=forms.PasswordInput(attrs={
                'id':"id_new_password2", 
                'class':"ctrlHolder",
                'placeholder': 'Enter Confirm Password ',
            }))
        class Meta:
            model = User
 
 
 
 
# <=========== Vendor Profile Forms =============>           
class Admin_profile_form(forms.ModelForm):
    class Meta:
        model = Vendor_profile
        exclude = ['user']
        widgets = {
            'first_name' : forms.TextInput(attrs={
                'id':"first_name", 
                'class':"form-control",
                'placeholder': 'Enter your First name', 
            }),
            'last_name' : forms.TextInput(attrs={
                'id':"first_name", 
                'class':"form-control",
                'placeholder': 'Enter your last_name', 
            }),
            'age' : forms.NumberInput(attrs={
                'id':"age", 
                'class':"form-control",
                'placeholder': 'Enter your age', 
            }),
            'gender' : forms.Select(attrs={
                'id':"gender", 
                'class':"form-control",
                'placeholder': 'Enter your gender', 
            }),
            'phone' : forms.NumberInput(attrs={
                'id':"phone", 
                'class':"form-control",
                'placeholder': 'Enter your Phone Number', 
            }),
            'c_name' : forms.TextInput(attrs={
                'id':"c_name", 
                'class':"form-control",
                'placeholder': 'Enter company name', 
            }),
            'c_email' : forms.EmailInput(attrs={
                'id':"c_email", 
                'class':"form-control",
                'placeholder': 'Enter company Email', 
            }),
            'c_website' : forms.URLInput(attrs={
                'id':"c_website", 
                'class':"form-control",
                'placeholder': 'Enter company website', 
            }),
            'c_des' : forms.Textarea(attrs={
                'id':"c_des", 
                'class':"form-control",
                'placeholder': 'Enter company address', 
            }),
            'address' : forms.Textarea(attrs={
                'id':"address", 
                'class':"form-control",
                'placeholder': 'Enter your address', 
            }),
            'location' : forms.Select(attrs={
                'id':"location", 
                'class':"form-control",
                'placeholder': 'Enter your location', 
            }),
            'image' : forms.FileInput(attrs={
                'id':"image", 
                'class':"form-control",
                # 'placeholder': 'Enter your location', 
            }),
        }


class User_form(forms.ModelForm):
    username = forms.CharField(required=True, disabled=True, label_suffix="", widget=forms.TextInput(attrs={
        'id':"username", 
        'class':"form-control",
        'placeholder': 'Enter Username',
    })) 
    email = forms.EmailField(required=True, disabled=True,  label_suffix="", widget=forms.EmailInput(attrs={
        'id':"username", 
        'class':"form-control",
        'placeholder': 'Enter Email',
    }))  
    class Meta:
        model = User
        fields = ['username','email']




# <=========== Vendor Pruduct Upload Forms =============>                  
class Product_from(forms.ModelForm):
    class Meta:
        model = Upload_product
        exclude = ['user']
        widgets = {
            'product_name' : forms.TextInput(attrs={
                'class':"form-control",
                'placeholder': 'Enter Product name', 
            }),
            'product_price' : forms.NumberInput(attrs={ 
                'class':"form-control",
                'placeholder': 'Enter Product Price', 
            }),
            'categories' : forms.Select(attrs={ 
                'class':"form-control",
                'placeholder': 'Enter Product Categories', 
            }),
            'date' : forms.DateTimeInput(attrs={ 
                'class':"form-control",
                'placeholder': 'Enter date', 
            }),
            'product_photo' : forms.FileInput(attrs={
                'class':"form-control",
                'placeholder': 'Enter Product Photo', 
            }),
            'stock' : forms.NumberInput(attrs={ 
                'class':"form-control",
                'placeholder': 'Enter Product Stock', 
            }),
            'description' : forms.Textarea(attrs={ 
                'class':"form-control",
                'placeholder': 'Enter Product Description', 
            }),
            'old_price' : forms.NumberInput(attrs={ 
                'class':"form-control",
                'placeholder': 'Enter Product Price', 
            }),
        }