from django import forms
from .models import Product
from .models import ProductVariation
from .models import Payment
from django.forms import inlineformset_factory
from .models import ProductImage

ProductVariationFormSet = inlineformset_factory(Product, ProductVariation, fields=('variation_code', 'quantity'), extra=1)
ProductImageFormSet = inlineformset_factory(
    Product, ProductImage,
    fields=('image',), extra=3, can_delete=True
)
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'brand', 'name', 'category','description', 'price','quantity', 'min_stock', 'max_stock', 'skin_type', 'skin_condition', 'skin_tone',
            'surface_tones', 'skin_texture', 'sensitivity_level']

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255, widget=forms.Textarea(attrs={'placeholder': 'Enter your address'}))
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    zipcode = forms.CharField(max_length=10)
    receipt = forms.FileField(required=True)


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class PaymentForm(forms.ModelForm):
    class meta:
        model = Payment
        fields = ['receipt']


        