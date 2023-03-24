from django import forms
from .models import Order, Customer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

class Checkoutform(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "ordered_by",
            "shipping_address",
            "mobile",
            "email",
        ]
            
class CustomerRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),label=("Username"),required=True)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),label=("Password"),required=True)
    email = forms.CharField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'email'}),label=("Email"),required=True)
    full_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'full name'}),label=("Full name"),required=True)
    address = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'address'}),label=("Address"),required=True)

    class Meta:
        model = Customer
        fields = ["username", "password","email","full_name", "address"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username

class login_form(AuthenticationForm):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'username'}),label=("Username"),required=True)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),label=("Password"),required=True)
