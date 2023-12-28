from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms

class CustomUserForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Username','style':'width:280px;'}))
    email=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Enter Enter Email ID','style':'width:280px;'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Passowrd','style':'width:280px;'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Confirm Password','style':'width:280px;'}))
    
    
    
    class Meta:
        model=User
        fields=('id','username','email')

    

class PhoneNumberForm(forms.Form):
    phone_number = forms.CharField(label='Phone Number', max_length=10)

class PinChangeForm(forms.Form):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput())
    

class PassChangeForm(forms.Form):
    password = forms.CharField( widget=forms.PasswordInput())

class NumChangeForm(forms.Form): 
    phone = forms.CharField(max_length=10,label='Phone Number')



class TransferForm(forms.Form):
    
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

class PinForm(forms.Form):
    pin = forms.CharField(max_length=4, widget=forms.PasswordInput())


