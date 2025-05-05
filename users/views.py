

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, CustomerForm
from users.models import User, Customer
from django.contrib.auth.decorators import login_required



def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('store:homepage')
    else:
        form = SignupForm()
    return render(request, 'register/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                if user.is_staff or user.is_superuser:
                    return redirect ('dashboard:homeadmin')
                else:
                  return redirect('store:homepage')
    else:
        form = AuthenticationForm()
    return render(request, 'register/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('store:homepage')

@login_required
def customer_profile(request):
    customer, created = Customer.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_profile')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customerprofile.html', {'form': form, 'customer': customer})
