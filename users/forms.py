from django.contrib.auth.forms import UserCreationForm
from django import forms
from users.models import User, Customer
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['phone_number', 'gender', 'profile_picture']
