from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserChangeForm,PasswordChangeForm
from django.db import models
from django.db.models import fields
from django.forms import widgets
from .models import *
from django.contrib.auth.models import User

class CheckOutForm(forms.ModelForm):
    class Meta:
        model= Order
        fields=["ordered_by","shipping_address", "mobile","email","payment_method"]

        widgets= {
            'ordered_by':forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address':forms.TextInput(attrs={'class':'form-control'}),
            'mobile':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'payment_method':forms.Select(attrs={'class':'form-control'}),
            
            
        }

class CustomerRegistrationForm(forms.ModelForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email= forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model=Customer
        fields=["username", "password", "email", "full_name","address","mobile"]
        widgets= {
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name..'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter address..'}),
            'mobile':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number..'}),
        }

    def clean_username(self):
        uname=self.cleaned_data.get("username")
        if User.objects.filter(username=uname).exists():
            raise forms.ValidationError("Customer with this username  already exists.")

        return uname

    def clean_email(self):
        em=self.cleaned_data.get("email")
        if User.objects.filter(email=em).exists():
            raise forms.ValidationError("Customer with this email already exists.")

        return em

class CustomerLoginForm(forms.Form):
    username= forms.CharField(widget=widgets.TextInput(attrs={'class':'form-control','placeholder':'Enter the username...'}))
    password= forms.CharField(widget=widgets.PasswordInput(attrs={'class':'form-control','placeholder':'Enter the password...'}))



class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "multiple": True
    }))
    class Meta:
        model = Product
        fields = ["title", "slug","image", "marked_price",
                  "selling_price","quantity_unit", "description"]
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product title here..."
            }),
            "slug": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the unique slug here..."
            }),
            
            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "marked_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Marked price of the product..."
            }),
            "selling_price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Selling price of the product..."
            }),
            "quantity_unit": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter the product quantity unit here..."
            }),
           

        }

class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "Enter the email used in customer account..."
    }))

    def clean_email(self):
        e = self.cleaned_data.get("email")
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError(
                "Customer with this account does not exists..")
        return e

class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password',
    }), label="New Password")
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password',
    }), label="Confirm New Password")

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_new_password = self.cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New Passwords did not match!")
        return confirm_new_password


class ContactUsForm(forms.ModelForm):

    class Meta:
        model= ContactUs
        fields=['first_name','last_name','email','subject','message']

        widgets={
            'first_name':forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Enter your first name...',
                        }),
            'last_name':forms.TextInput(attrs={
                        'class': 'form-control',
                        'placeholder': 'Enter your last name...',
                        }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your email address...'}),

            'subject':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter your subject...'}),

            'message':forms.Textarea(attrs={
                'class':'form-control',
                'placeholder':'Enter your message...'}),

        }
            

class SettingsForm(UserChangeForm):
    username= forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email= forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model=User
        fields=["username","email"]
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'})

        }

class UpdateProfileForm(forms.ModelForm):  
    class Meta:
        model=Customer
        fields=["full_name","address","mobile"]
        widgets= {
            'full_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Full Name..'}),
            'address':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter address..'}),
            'mobile':forms.TextInput(attrs={'class':'form-control','placeholder':'Enter mobile number..'}),
        }     

class PasswordChangingForm(PasswordChangeForm):
    old_password= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password1= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))
    new_password2= forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','type':'password'}))

    class Meta:
        models=User
        fields=['old_password','new_password1','new_password2']
