from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from users.models import User, Employee, CustomerProfile
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
from django.utils.timezone import now, timedelta
from django.template.loader import get_template
from weasyprint import HTML
import tempfile
from xhtml2pdf import pisa
import csv
from django.utils import timezone
from datetime import timedelta
from django.db.models import FloatField



# Create your views here.
@login_required
def homeadmin(request):
    total_users = CustomerProfile.objects.count()
    total_products = Product.objects.count()
    today = now().date()
    orders_today = Order.objects.filter(date_ordered__date=today).count()
    revenue_today = Order.objects.filter(date_ordered__date=today, complete=True).aggregate(
        total=Sum('total'))['total'] or 0
    
    total_revenue = Order.objects.filter(complete=True).aggregate(
    total=Sum('total'))['total'] or 0


    recent_orders = Order.objects.filter(complete=True).order_by('-date_ordered')[:3]
    low_stock_products = Product.objects.filter(quantity__lt=10)
    new_users = CustomerProfile.objects.order_by('-created_at')[:3]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'orders_today': orders_today,
        'revenue_today': revenue_today,
        'total_revenue':total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'new_users': new_users,
    }
    return render(request, 'dashboard/homeadmin.html', context)

@staff_member_required
def homestaff(request):
    total_users = CustomerProfile.objects.count()
    total_products = Product.objects.count()
    today = now().date()
    orders_today = Order.objects.filter(date_ordered__date=today).count()
    revenue_today = Order.objects.filter(date_ordered__date=today, complete=True).aggregate(
        total=Sum('total'))['total'] or 0
    
    total_revenue = Order.objects.filter(complete=True).aggregate(
    total=Sum('total'))['total'] or 0


    recent_orders = Order.objects.filter(complete=True).order_by('-date_ordered')[:3]
    low_stock_products = Product.objects.filter(quantity__lt=10)
    new_users = CustomerProfile.objects.order_by('-created_at')[:3]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'orders_today': orders_today,
        'revenue_today': revenue_today,
        'total_revenue':total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'new_users': new_users,
    }
    return render(request,'dashboard/homestaff.html', context)

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
def menambahproduk(request):
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

    return render(request, 'dashboard/menambahproduk.html', {
        'form': form,
        'image_formset': image_formset,
        'variation_formset': variation_formset,
        'action': 'Add',
    })

# Edit a product
@staff_member_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    ImageFormSet = inlineformset_factory(
        Product, 
        ProductImage, 
        form=ProductImageForm,
        extra=1,
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
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_formset = ImageFormSet(request.POST, request.FILES, instance=product, prefix='images')
        variation_formset = VariationFormSet(request.POST, instance=product, prefix='variations')

        if form.is_valid() and image_formset.is_valid() and variation_formset.is_valid():
            form.save()
            image_formset.save()
            variation_formset.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('dashboard:manageproducts')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
        image_formset = ImageFormSet(instance=product, prefix='images')
        variation_formset = VariationFormSet(instance=product, prefix='variations')

    return render(request, 'dashboard/editproduk.html', {
        'form': form,
        'image_formset': image_formset,
        'variation_formset': variation_formset,
        'product': product,
    })


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

@staff_member_required
def view_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)
    variations = ProductVariation.objects.filter(product=product)
    
    return render(request, 'dashboard/viewproduct.html', {
        'product': product,
        'images': images,
        'variations': variations,
    })

@staff_member_required
def staff_view_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    images = ProductImage.objects.filter(product=product)
    variations = ProductVariation.objects.filter(product=product)
    
    return render(request, 'dashboard/staffviewproduct.html', {
        'product': product,
        'images': images,
        'variations': variations,
    })


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


@staff_member_required
def manageorder(request):
    status_filter = request.GET.get('status', None)
    
    if status_filter:
        orders = Order.objects.filter(status=status_filter, complete=True).order_by('-date_ordered')
    else:
        orders = Order.objects.filter(complete=True).order_by('-date_ordered')

    paginator = Paginator(orders, 10) 
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

def get_report_context(request):
    date_range = request.GET.get('date_range', '7')
    try:
        days = int(date_range)
        start_date = timezone.now() - timedelta(days=days)
    except ValueError:
        start_date = timezone.now() - timedelta(days=7)

    orders = Order.objects.filter(date_ordered__gte=start_date, complete=True)
    order_items = OrderItem.objects.filter(order__in=orders)

    order_items = order_items.annotate(
        line_revenue=F('quantity') * F('product__price')
    )

    total_revenue = orders.aggregate(total=Sum('total'))['total'] or 0
    total_orders = orders.count()
    aov = total_revenue / total_orders if total_orders > 0 else 0

    prev_start = start_date - (timezone.now() - start_date)
    prev_orders = Order.objects.filter(
        date_ordered__gte=prev_start,
        date_ordered__lt=start_date,
        complete=True
    )
    prev_revenue = prev_orders.aggregate(total=Sum('total'))['total'] or 0
    revenue_growth = ((total_revenue - prev_revenue) / prev_revenue * 100) if prev_revenue > 0 else 0

    customers = User.objects.filter(order__in=orders).distinct()
    new_customers = customers.filter(date_joined__gte=start_date).count()
    returning_customers = customers.count() - new_customers

    # Product performance (Top Products)
    top_products = order_items.values(
        'product__name', 'product__category'
    ).annotate(
        quantity_sold=Sum('quantity'),
        revenue=Sum('line_revenue', output_field=FloatField())
    ).order_by('-revenue')[:10]

    # Category performance
    category_performance = order_items.values(
        'product__category'
    ).annotate(
        revenue=Sum('line_revenue', output_field=FloatField()),
        count=Count('id')
    ).order_by('-revenue')

    # Sales over time data
    sales_over_time = orders.extra(
        {'date': "date(date_ordered)"}
    ).values('date').annotate(
        revenue=Sum('total'),
        orders=Count('id')
    ).order_by('date')

    # Orders table data (limit to recent 50)
    orders_table = orders.select_related('user').order_by('-date_ordered')[:50]

    # Products sold table
    products_sold = order_items.values(
        'product__name', 'product__category'
    ).annotate(
        quantity=Sum('quantity'),
        revenue=Sum('line_revenue', output_field=FloatField())
    ).order_by('-quantity')

    # Customer spending (Top 50 customers)
    customer_spending = orders.values(
        'user__first_name', 'user__last_name', 'user__email'
    ).annotate(
        total_spent=Sum('total'),
        order_count=Count('id')
    ).order_by('-total_spent')[:50]

    context = {
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'aov': aov,
        'revenue_growth': revenue_growth,
        'customer_count': customers.count(),
        'new_customers': new_customers,
        'returning_customers': returning_customers,
        'top_products': top_products,
        'category_performance': category_performance,
        'sales_over_time': sales_over_time,
        'orders_table': orders_table,
        'products_sold': products_sold,
        'customer_spending': customer_spending,
        'date_range': date_range,
        'start_date': start_date,
    }

    return context

@staff_member_required
def sales_report(request):
    context = get_report_context(request)
    return render(request, 'dashboard/report.html', context)

@staff_member_required
def export_report(request, format_type):
    context = get_report_context(request)
    if format_type == 'pdf':
        template = get_template('dashboard/report_pdf.html')
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        pisa_status = pisa.CreatePDF(html, dest=response)
        if pisa_status.err:
            return HttpResponse('Error generating PDF')
        return response

    elif format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
        writer = csv.writer(response)
        # Write header
        writer.writerow([
            'Metric', 'Value'
        ])
        # Write metrics
        writer.writerow(['Total Revenue', context['total_revenue']])
        writer.writerow(['Total Orders', context['total_orders']])
        writer.writerow(['Average Order Value', context['aov']])
        writer.writerow(['Revenue Growth (%)', context['revenue_growth']])
        writer.writerow(['Number of Customers', context['customer_count']])
        writer.writerow(['New Customers', context['new_customers']])
        writer.writerow(['Returning Customers', context['returning_customers']])
        writer.writerow([])
        writer.writerow(['Top Products', 'Quantity Sold', 'Revenue'])
        for product in context['top_products']:
            writer.writerow([
                product['product__name'],
                product['quantity_sold'],
                product['revenue']
            ])
        return response
    
@staff_member_required
def staffviewproducts(request):
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

    return render(request, 'dashboard/staffproduct.html', context)
    
