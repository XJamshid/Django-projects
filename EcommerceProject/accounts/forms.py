from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from .models import Customer

class CustomerCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(
        region="UZ"
    )
    class Meta:
        model=Customer
        fields=('username','first_name','last_name','date_of_birth','email','phone_number')

class CustomerChangeForm(UserChangeForm):
    password = None
    phone_number = PhoneNumberField(
        region="UZ"
    )
    class Meta:
        model=Customer
        fields=('username','first_name','last_name','date_of_birth','email','phone_number')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)