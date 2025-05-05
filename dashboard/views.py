from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from users.models import User, Employee
from store.models import Product, ProductAdmin
from django.http import HttpResponse
from django.contrib import messages




# Create your views here.
@staff_member_required
def homeadmin(request):
    return render(request,'dashboard/homeadmin.html')

@staff_member_required
def manageusers(request):
    # Fetch customers (non-staff, non-superuser users)
    customers = User.objects.filter(is_staff=False, is_superuser=False)
    
    # Fetch employees, now using the user relationship
    employees = Employee.objects.filter(user__is_staff=True)  # Filter employees who are associated with staff users

    return render(request, 'dashboard/manageusers.html', {
        'customers': customers,
        'employees': employees,
    })

@staff_member_required
def manageproducts(request):
    return render(request, 'dashboard/manageproducts.html')

@staff_member_required
def generatereport(request):
    return render(request, 'dashboard/generatereports.html')

def addstaff(request):
    if request.method == 'POST':
        # Handle adding the new staff member (create Employee instance, etc.)
        name = request.POST.get('name')
        email = request.POST.get('email')
        position = request.POST.get('position')
        # Add more fields as needed
        
        # Assuming you have a staff creation form, you can add staff here
        new_staff = Employee(name=name, email=email, position=position)
        new_staff.save()

        return HttpResponse("Staff added successfully!")  # Or redirect to another page
    return render(request, 'dashboard/addstaff.html')  # The page to add new staff

def addadmin(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_hired = request.POST['date_hired'] 

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
        )

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'dashboard/addadmin.html') 

        user.is_staff = True
        user.is_superuser = True
        user.save()

        employee = Employee(name=username, email=email, position= "Admin")
        employee.save()

        return HttpResponse("Admin added successfully!")  # Redirect to another page as needed
    return render(request, 'dashboard/addadmin.html')
