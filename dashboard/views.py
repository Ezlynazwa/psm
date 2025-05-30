from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from users.models import User, Employee
from store.models import Product, ProductVariation ,ProductImage, Order, OrderItem 
from django.http import HttpResponse
from django.contrib import messages
from store.forms import ProductImageFormSet 
from .forms import ProductForm, OrderStatusForm, TrackingNumberForm, ParcelImageForm
from store.forms import  ProductImageForm, ProductVariationForm
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from django.db.models import Sum, Count, F
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test



# Create your views here.
@staff_member_required
def homeadmin(request):
    return render(request,'dashboard/homeadmin.html')

@staff_member_required
def homestaff(request):
    return render(request,'dashboard/homestaff.html')

@staff_member_required
def staffproduct(request):
    return render(request, 'dashboard/staffproduct.html' )

@staff_member_required
def manageorder(request):
    return render(request, 'manageorder.html')

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
        'skin_tone': ProductVariation.SKIN_TONES,
        'surface_tone': ProductVariation.SURFACE_TONES,
    }

    return render(request, 'dashboard/manageproducts.html', context)


@staff_member_required
def generatereport(request):
    return render(request, 'dashboard/generatereports.html')

@staff_member_required
def add_product(request):
    ImageFormSet = inlineformset_factory(
        Product, 
        ProductImage, 
        form=ProductImageForm,
        extra=1,  # Start with 1 empty form
        max_num=10,
        can_delete=True
    )
    
    VariationFormSet = inlineformset_factory(
        Product,
        ProductVariation,
        form=ProductVariationForm,
        extra=1,
        can_delete=True
    )

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        image_formset = ImageFormSet(request.POST, request.FILES, prefix='images')
        variation_formset = VariationFormSet(request.POST, prefix='variations')

        if form.is_valid() and image_formset.is_valid() and variation_formset.is_valid():
            product = form.save()
            image_formset.instance = product
            variation_formset.instance = product
            image_formset.save()
            variation_formset.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard:manageproducts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
        image_formset = ImageFormSet(queryset=ProductImage.objects.none(), prefix='images')
        variation_formset = VariationFormSet(queryset=ProductVariation.objects.none(), prefix='variations')

    return render(request, 'dashboard/product_form.html', {
        'form': form,
        'image_formset': image_formset,
        'variation_formset': variation_formset,
        'action': 'Add',
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

@staff_member_required
def delete_product(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('dashboard:manageproducts')

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('dashboard:manageproducts')

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


def analytics_dashboard(request):
    # Time range filter (default: 30 days)
    days = int(request.GET.get('days', 30))
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Sales Metrics
    orders = Order.objects.filter(
        date_ordered__range=(start_date, end_date),
        complete=True
    )
    total_revenue = orders.aggregate(total=Sum('orderitem__product__price'))['total'] or 0
    total_orders = orders.count()
    aov = total_revenue / total_orders if total_orders > 0 else 0

    # Revenue growth calculation
    prev_period = orders.filter(
        date_ordered__range=(start_date - timedelta(days=days), start_date)
    ).aggregate(total=Sum('orderitem__product__price'))['total'] or 0
    revenue_growth = ((total_revenue - prev_period) / prev_period * 100) if prev_period > 0 else 0

    # Customer Metrics
    customers = Customer.objects.filter(order__date_ordered__range=(start_date, end_date)).distinct()
    total_customers = customers.count()
    new_customers = customers.filter(date_joined__range=(start_date, end_date)).count()
    returning_customers = total_customers - new_customers

    # Top Products
    top_products = Product.objects.filter(
        orderitem__order__date_ordered__range=(start_date, end_date)
    ).annotate(
        total_revenue=Sum(F('orderitem__quantity') * F('price'))
    ).order_by('-total_revenue')[:5]

    # Inventory Alerts
    low_stock_count = Product.objects.filter(quantity__lt=F('min_stock')).count()
    out_of_stock_count = Product.objects.filter(quantity=0).count()

    # Dynamic Category Breakdown
    category_data = (
        OrderItem.objects
        .filter(order__date_ordered__range=(start_date, end_date))
        .values('product__category')  # Group by category
        .annotate(total_sales=Sum(F('quantity') * F('product__price')))
        .order_by('-total_sales')
    )

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'aov': aov,
        'revenue_growth': revenue_growth,
        'total_customers': total_customers,
        'new_customers': new_customers,
        'returning_customers': returning_customers,
        'top_product_names': [p.name for p in top_products],
        'top_product_revenues': [float(p.total_revenue) for p in top_products],
        'category_labels': ['Skincare', 'Makeup', 'Haircare', 'Fragrance'],
        'category_values': [45, 30, 15, 10],  # Replace with real data
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'category_labels': [item['product__category'] for item in category_data],
        'category_values': [float(item['total_sales']) for item in category_data],
    }
    return render(request, 'dashboard/generatereports.html', context)

@staff_member_required
def manageorder(request):
    # Get filter parameter
    status_filter = request.GET.get('status', None)
    
    # Get all orders or filtered orders
    if status_filter:
        orders = Order.objects.filter(status=status_filter).order_by('-date_ordered')
    else:
        orders = Order.objects.all().order_by('-date_ordered')

    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status_filter': status_filter,
    }
    return render(request, 'dashboard/manageorder.html', context)

@staff_member_required
def orderdetail(request, id):
    order = get_object_or_404(Order, id=id)
    
    if request.method == 'POST':
        if 'update_status' in request.POST:
            status_form = OrderStatusForm(request.POST, instance=order)
            if status_form.is_valid():
                status_form.save()
                return redirect('dashboard:orderdetail', id=order.id)
        elif 'update_tracking' in request.POST:
            tracking_form = TrackingNumberForm(request.POST, instance=order)
            if tracking_form.is_valid():
                tracking_form.save()
                return redirect('dashboard:orderdetail', id=order.id)
        elif 'upload_parcel' in request.POST:
            parcel_form = ParcelImageForm(request.POST, request.FILES, instance=order)
            if parcel_form.is_valid():
                parcel_form.save()
                return redirect('dashboard:orderdetail', id=order.id)
    else:
        status_form = OrderStatusForm(instance=order)
        tracking_form = TrackingNumberForm(instance=order)
        parcel_form = ParcelImageForm(instance=order)

    order_items = order.orderitem_set.all()

    # ✅ Check if receipt exists and is PDF
    payment = getattr(order, 'payment', None)
    is_pdf = payment and payment.receipt and payment.receipt.name.lower().endswith('.pdf')

    context = {
        'order': order,
        'order_items': order_items,
        'status_form': status_form,
        'tracking_form': tracking_form,
        'parcel_form': parcel_form,
        'is_pdf': is_pdf,
    }
    return render(request, 'dashboard/orderdetail.html', context)
