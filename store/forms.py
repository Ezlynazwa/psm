from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'quantity', 
            'min_stock', 'max_stock', 'skin_type', 
            'skin_condition', 'skin_tone', 
            'skin_texture', 'sensitivity_level','category','variation_code','surface_tones','images'
        ]

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'placeholder': 'Enter your address'}))
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=10)
