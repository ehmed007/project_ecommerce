from django import forms
from .models import Order, Customer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    username = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.CharField(widget=forms.EmailInput())
    
    class Meta:
        model = Customer
        fields = ["username", "password","email","full_name", "address"]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already exists')
        return username
