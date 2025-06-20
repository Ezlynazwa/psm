

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, CustomerForm, StaffForm, AdminForm
from .models import User, CustomerProfile, Employee
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

                if user.is_superuser:
                    return redirect ('dashboard:homeadmin')
                elif user.is_staff:
                    return redirect ('dashboard:homestaff')
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
    customer, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('users:customer_profile')
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'customerprofile.html', {'form': form, 'customer': customer})

@login_required
def staff_profile(request):
    staff, created = Employee.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('users:staff_profile')
    else:
        form = StaffForm(instance=staff)

    return render(request, 'staffprofile.html', {'form': form, 'staff': staff})

@login_required
def admin_profile(request):
    try:
        admin=Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        admin=None

    if request.method == 'POST':
        form = AdminForm(request.POST, request.FILES, instance=admin)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.user = request.user
            admin.save()
            return redirect('users:admin_profile')
    else:
        form = AdminForm(instance=admin)

    return render(request, 'adminprofile.html', {'form': form, 'admin': admin})