from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User, CustomerProfile, Employee

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

from django import forms
from .models import CustomerProfile

class CustomerForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = [
            'phone_number',
            'first_name',
            'last_name',
            'email',
            'preferred_contact_method',
            'gender',
            'date_of_birth',
            'profile_picture',

        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'ethical_preferences': forms.TextInput(attrs={'placeholder': "e.g. vegan, cruelty_free"}),
        }

class StaffForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'contact',
            'name',
            'first_name',
            'last_name',
            'email',
            'date_hired',
            'password',
            'photo',
        ]
        widgets = {
            'date_hired': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(render_value=True),
        }

class AdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            'contact',
            'name',
            'first_name',
            'last_name',
            'email',
            'password',
            'photo',
            'date_hired', 

        ]
        widgets = {
        'date_hired': forms.DateInput(attrs={'type': 'date'}),
        'password': forms.PasswordInput(render_value=True),
    }
