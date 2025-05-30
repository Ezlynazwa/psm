from django import forms
from store.models import Product, ProductVariation, Order
from users.models import Employee
from django.forms import inlineformset_factory
from store.models import ProductImage
from store.forms import ProductImageForm, ProductVariationForm 

ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=1,
    can_delete=True,
    max_num=10
)

ProductVariationFormSet = inlineformset_factory(
    Product,
    ProductVariation,
    form=ProductVariationForm,
    extra=1,
    can_delete=True
)

# handles add and edit product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'brand', 'name', 'category','description', 'size', 'texture',  
            'price','quantity', 'min_stock', 'max_stock', 
            'skin_type', 'skin_condition', 'skin_texture', 
            'sensitivity_level', 'suitable_for', 'finish', 'is_vegan', 'long_last', 'waterproof' , 'is_cruelty_free'
            , 'spf', 'coverage', 
          ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),}

# handles Add & Edit Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 
                  'password', 
                  'position', 
                  'contact', 
                  'email', 
                  'date_hired', 
                  'photo']
        
        widgets = {
            'password': forms.PasswordInput(),  # Mask password input
            'date_hired': forms.DateInput(attrs={'type': 'date'})  # Date picker
        }

        
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class TrackingNumberForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['tracking_number']
        widgets = {
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ParcelImageForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['parcel_image']
        widgets = {
            'parcel_image': forms.FileInput(attrs={'class': 'form-control'}),
        }