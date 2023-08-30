from django import forms
from .models import *



class ContactForm(forms.ModelForm):
    First_name = forms.CharField(label='', label_suffix="", widget=forms.TextInput(attrs={ 
            'class':"input-style mb-20",
            'placeholder': "First Name",
        }))
    Phone = forms.IntegerField(label='', label_suffix="", widget=forms.NumberInput(attrs={ 
            'class':"input-style mb-20",
            'placeholder': "Your Phone",
        }))
    subject = forms.CharField(label='', label_suffix="", widget=forms.TextInput(attrs={ 
            'class':"input-style mb-20",
            'placeholder': "Subject",
        }))

    email = forms.EmailField(label='', label_suffix="", widget=forms.EmailInput(attrs={ 
            'class':"input-style mb-20",
            'placeholder': "Your Email",
        }))
    message = forms.CharField(label='', label_suffix="", widget=forms.Textarea(attrs={ 
            'class':"input-style mb-20",
            'placeholder': "Message",
        }))
    class Meta:
        model = Contact
        fields = "__all__"
        


       
# class Subscribeform(forms.ModelForm):
#     # email = forms.EmailField(label='', label_suffix="", widget=forms.EmailInput(attrs={ 
#     #         # 'id' : "subscribe-input-2",
#     #         'class':"input-style mb-20",
#     #         'placeholder': "Your emaill address",
#     #     }))
#     class Meta:
#         model = Subscribe
#         fields = "__all__"
#         # widgets = {
#         #     'email' : forms.EmailInput(attrs={
#         #         # 'class':"form-subcriber d-flex selector-2",
#         #         # 'placeholder': "Your emaill address",
#         #         # 'type' : "email" 
#         #     }),
#         # }