from django import forms
from .models import Product
from .models import ProductVariation
from .models import Payment
from django.forms import inlineformset_factory
from .models import ProductImage

ProductVariationFormSet = inlineformset_factory(
    Product, ProductVariation, 
    fields=(
    'variation_code', 
    'quantity',
    'skin_tone',
    'surface_tones'),
    extra=10,
    can_delete=True)

ProductImageFormSet = inlineformset_factory(
    Product, 
    ProductImage,
    fields=('image',), 
    extra=10, 
    can_delete=True)

class CheckoutForm(forms.Form):
    PAYMENT_CHOICES = [
        ('qr', 'QR Code'),
    ]
    address = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'placeholder': 'Enter your address'}),
        required=False
    )
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    zipcode = forms.CharField(max_length=10, required=False)

    selected_address = forms.IntegerField(required=False)
    add_new_address = forms.BooleanField(required=False)

    receipt = forms.FileField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        add_new = self.data.get('add_new_address') == 'on'
        if add_new:
            if not cleaned_data.get('address'):
                self.add_error('address', 'This field is required when adding new address')
            if not cleaned_data.get('city'):
                self.add_error('city', 'This field is required when adding new address')
            if not cleaned_data.get('state'):
                self.add_error('state', 'This field is required when adding new address')
            if not cleaned_data.get('zipcode'):
                self.add_error('zipcode', 'This field is required when adding new address')
        return cleaned_data



class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['receipt']

class ProductVariationForm(forms.ModelForm):
    class Meta:
        model = ProductVariation
        fields = [
            'variation_code', 
            'quantity', 
            'skin_tone', 
            'surface_tones']
        