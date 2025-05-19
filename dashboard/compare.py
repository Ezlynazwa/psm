from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from users.models import User, Employee
from store.models import Product, ProductImage, ProductVariation 
from django.http import HttpResponse
from django.contrib import messages
from .forms import ProductForm
from store.forms import ProductImageFormSet, ProductVariationFormSet
from django.forms import modelformset_factory



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

# Add a product
@staff_member_required

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        image_formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.none())
        variation_formset = ProductVariationFormSet(request.POST)
        
        if form.is_valid() and image_formset.is_valid() and variation_formset.is_valid():
            product = form.save()
            images = image_formset.save(commit=False)
            for image in images:
                image.product = product
                image.save()

            variations = variation_formset.save(commit=False)
            for var in variations:
                var.product = product
                var.save()

            return redirect('dashboard:manageproducts')
    else:
        form = ProductForm()
        image_formset = ProductImageFormSet(queryset=ProductImage.objects.none())
        variation_formset = ProductVariationFormSet()

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'formset': image_formset,
        'variation_formset': variation_formset,
        'action': 'Add',
    })


# Edit a product
@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard:manage_products')
        else:
           form = ProductForm(instance=product)
        return render(request, 'dashboard/product_form.html', {'form': form, 'action': 'Edit'})

# Delete a product
@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:manage_products')
    return render(request, 'dashboard/delete_confirm.html', {'product': product})



@staff_member_required
def generatereport(request):
    return render(request, 'dashboard/generatereports.html')

def addstaff(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        contact = request.POST.get('contact')
        username = request.POST.get('username')
        password = request.POST.get('password')
        date_hired = request.POST.get('date_hired')
        photo = request.FILES.get('photo')


        if not all([name, email, position,contact, username, password, date_hired]):
            messages.error(request, "Please fill in all fields.")
            return redirect('dashboard:addstaff')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return redirect('dashboard:addstaff')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            is_staff=True,
            first_name=first_name,
            last_name=last_name,
            photo=photo
        )
        user.save()

        # Create employee profile and link to user
        employee = Employee.objects.create(
            user=user,
            name=name,
            email=email,
            contact=contact,
            position=position,
            date_hired=date_hired, 
            first_name=first_name,
            last_name=last_name,
            photo=photo
        )

        print("DEBUG - POST:", request.POST)
        messages.success(request, "Staff added succesfully!")
        return redirect('dashboard:manageusers')
    return render(request, 'dashboard/addstaff.html')  # The page to add new staff

def addadmin(request):
    if request.method == 'POST': 
        username = request.POST('username')
        password = request.POST('password')
        contact = request.POST('contact')
        email = request.POST('email')
        first_name = request.POST('first_name')
        last_name = request.POST('last_name')
        date_hired = request.POST('date_hired')

        

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,
        )
        user.save()
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'dashboard/addadmin.html') 

        # Create Employee profile with user linked
        employee = Employee.objects.create(
            user=user,
            name=f"{first_name} {last_name}",
            email=email,
            position="Admin",
            date_hired=date_hired
        )

        messages.success(request, "Admin added successfully!")
        return redirect('dashboard:manageusers')
    return render(request, 'dashboard/addadmin.html')
