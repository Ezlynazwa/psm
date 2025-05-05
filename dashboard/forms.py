from django import forms
from store.models import Product
from users.models import Employee
# handles add and edit product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'quantity', 'min_stock', 'max_stock',
            'variation_code', 'skin_type', 'skin_condition', 'skin_tone',
            'surface_tones', 'skin_texture', 'sensitivity_level', 'images',
            'category', 'digital'
        ]

# handles Add & Edit Employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'password', 'position', 'contact', 'email', 'date_hired', 'photo']
        widgets = {
            'password': forms.PasswordInput(),  # Mask password input
            'date_hired': forms.DateInput(attrs={'type': 'date'})  # Date picker
        }

