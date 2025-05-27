from store.models import Product
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from users.models import User, Employee
from store.models import ProductVariation ,ProductImage
from django.http import HttpResponse
from django.contrib import messages
from store.forms import ProductVariationFormSet, ProductImageFormSet 
from django.forms import modelformset_factory
from .forms import ProductForm 




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
    products = Product.objects.all()
    categories = Product.objects.values_list('category', flat=True).distinct()

    category = request.GET.get('category')
    sort_option = request.GET.get('sort')

    if category:
        products = products.filter(category=category)

    if sort_option == 'price_asc':
        products = products.order_by('price')
    elif sort_option == 'price_desc':
        products = products.order_by('-price')
    elif sort_option == 'name_asc':
        products = products.order_by('name')
    elif sort_option == 'name_desc':
        products = products.order_by('-name')
    elif sort_option == 'latest':
        products = products.order_by('-created_at') 
    elif sort_option == 'oldest':
        products = products.order_by('created_at')

    context = {
        'products': products,
        'categories': categories,
        'skin_tone_choices': Product._meta.get_field('skin_tone').choices,
        'surface_tone_choices': Product._meta.get_field('surface_tones').choices,
    }

    return render(request, 'dashboard/manageproducts.html', context)


@staff_member_required
def generatereport(request):
    return render(request, 'dashboard/generatereports.html')

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
        'skin_tone_choices': Product._meta.get_field('skin_tone').choices,
        'surface_tone_choices': Product._meta.get_field('surface_tones').choices,
    })


# Edit a product
@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ProductImageFormSet(request.POST, request.FILES, queryset=ProductImage.objects.filter(product=product))

        if form.is_valid() and image_formset.is_valid():
            form.save()
            images = image_formset.save(commit=False)
            for image in images:
                image.product = product
                image.save()

            for obj in image_formset.deleted_objects:
                obj.delete()

            return redirect('dashboard:manageproducts')
    else:
        form = ProductForm(instance=product)
        image_formset = ProductImageFormSet(queryset=ProductImage.objects.filter(product=product))

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'formset': image_formset,
        'action': 'Edit'})

# Delete a product
@staff_member_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:manage_products')
    return render(request, 'dashboard/delete_confirm.html', {'product': product})


def addstaff(request):
    if request.method == 'POST':
        # Handle adding the new staff member (create Employee instance, etc.)

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        email = request.POST['email']
        position = request.POST['position']
        contact = request.POST['contact']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_hired = request.POST['date_hired'] 
        photo = request.FILES['photo'] 

        if not all([username, email, position,first_name, last_name, photo, contact, username, password, date_hired]):
            messages.error(request, "Please fill in all fields.")
            return redirect('dashboard:addstaff')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'dashboard/addstaff.html')
        
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            )
        
        user.is_staff = True
        user.save()

        employee = Employee(
            user=user,
            name=username, 
            password=password,
            email=email,
            position=position,
            contact=contact,
            photo=photo,
            first_name=first_name,
            last_name=last_name,
            date_hired=date_hired,
            )
        employee.save()

        messages.success(request, "Staff added successfully!")
        return redirect('dashboard:manageusers')  # Or redirect to another page
    return render(request, 'dashboard/addstaff.html')  # The page to add new staff

def addadmin(request):
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        contact = request.POST['contact']
        position = request.POST['position']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_hired = request.POST['date_hired'] 
        photo = request.FILES['photo'] 

        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose another one.')
            return render(request, 'dashboard/addadmin.html') 

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True,

        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        employee = Employee(
            user=user,
            name=username, 
            password=password,
            email=email,
            contact=contact,
            photo=photo,
            position=position,
            first_name=first_name,
            last_name=last_name,
            date_hired=date_hired,
            )
        employee.save()

        messages.success(request, 'Admin added successfully!')
        return redirect('dashboard:manageusers')  # Redirect to another page as needed
    
    return render(request, 'dashboard/addadmin.html')

