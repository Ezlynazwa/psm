from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User, CustomerProfile
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
            'preferred_contact_method',
            'gender',
            'date_of_birth',
            'profile_picture',
            'skin_type',
            'undertone',
            'surface_tone',
            'concerns',
            'sensitivity_level',
            'known_allergies',
            'preferred_finish',
            'preferred_coverage',
            'preferred_texture',
            'ethical_preferences',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'ethical_preferences': forms.TextInput(attrs={'placeholder': "e.g. vegan, cruelty_free"}),
        }
