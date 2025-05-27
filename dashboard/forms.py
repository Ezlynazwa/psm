from django import forms
from store.models import Product
from users.models import Employee
from django.forms import modelformset_factory
from store.models import ProductImage
from store.forms import ProductImageForm


ProductImageFormSet = modelformset_factory(
    ProductImage,
    form=ProductImageForm,
    extra=10,  
    can_delete=True,
)

# handles add and edit product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'brand', 'name', 'category','description', 'price','quantity', 'min_stock', 'max_stock', 'skin_type', 'skin_condition', 'skin_tone',
            'surface_tones', 'skin_texture', 'sensitivity_level'       ]

# handles Add & Edit Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'password', 'position', 'contact', 'email', 'date_hired', 'photo']
        widgets = {
            'password': forms.PasswordInput(),  # Mask password input
            'date_hired': forms.DateInput(attrs={'type': 'date'})  # Date picker
        }

