from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, ShippingAddress, ProductImage, ProductVariation
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from dashboard.forms import ProductForm
from .forms import CheckoutForm, PaymentForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages  
from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal





# Homepage view
def homepage(request):
    products = Product.objects.all()  # Fetch all products for the homepage
    product_data = []

    for product in products:
        images = product.product_images.all()
        first_image = images[0] if images else None
        product_data.append({
            'product': product,
            'image': first_image
        })

    return render(request, 'store/homepage.html', {'product_data': product_data})
    return HttpResponse("Hello, this is the homepage!")

# Catalog page view

def catalog(request):
    products = Product.objects.all()
    product_data = []

    for product in products:
        images = product.product_images.all()
        first_image = images[0] if images else None
        product_data.append({
            'product': product,
            'image': first_image
        })

    return render(request, 'store/catalog.html', {
        'product_data': product_data
    })


# View Product page view
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':

        if not request.user.is_authenticated:
            # Redirect to login page and return here after login
            login_url = f"{reverse('users/login')}?next={request.path}"
            return redirect('login_url')
        
        quantity = int(request.POST.get('quantity', 1))
        
        # Get or create an order for the user
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        
        # Add the item to the cart
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += quantity  # Increment the quantity
        order_item.save()

        return redirect('store:cart')  # Redirect to the cart page after adding the item
    
    images = product.product_images.all()

    return render(request, 'store/view_product.html', {
        'product': product,
        'images':images
        })


@login_required
def cart(request):
    if request.user.is_authenticated:
        # Ambil semua order yang belum lengkap untuk user ini
        orders = Order.objects.filter(user=request.user, complete=False).order_by('-date_ordered')
        
        # Buang order yang lebih, simpan hanya satu (paling terkini)
        if orders.count() > 1:
            orders.exclude(id=orders.first().id).delete()

        # Guna order yang kekal
        order = orders.first()
        items = order.orderitem_set.all()
        total = order.get_cart_total
        cart_items = order.get_cart_items
    else:
        items = []
        total = 0
        cart_items = 0

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total,
        'cart_items': cart_items,
        'order':order,
    })

@login_required
def checkout(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, user=request.user)
        saved_addresses = ShippingAddress.objects.filter(user=request.user)
        
        selected_item_ids = request.session.get('checkout_items', [])
        if not selected_item_ids:
            messages.error(request, "No items selected for checkout")
            return redirect('store:cart')
            
        selected_items = order.orderitem_set.filter(id__in=selected_item_ids)
        if not selected_items.exists():
            messages.error(request, "Selected items no longer available")
            return redirect('store:cart')
        
        subtotal = sum(item.get_total for item in selected_items)
        shipping = Decimal('8.00')
        total = subtotal + shipping

        if request.method == 'POST':
            form = CheckoutForm(request.POST, request.FILES)
            
            if form.is_valid():
                # Create a NEW order for the checked out items
                new_order = Order.objects.create(
                    user=request.user,
                    complete=True,
                    total=total,
                    status='pending'
                )
                try:
                    new_order.save()
                    print("New order saved successfully:", new_order.id)  # Debug
                except Exception as e:
                    print("ORDER SAVE ERROR:", e)  # Debug
                    messages.error(request, f"Order could not be saved: {str(e)}")
                    return redirect('store:cart')  # This might be triggering
                                
                # Copy selected items to new order
                for item in selected_items:
                    OrderItem.objects.create(
                        product=item.product,
                        order=new_order,
                        quantity=item.quantity
                    )
                
                # Process address
                if request.POST.get('add_new_address') == 'on':
                    shipping_address = ShippingAddress.objects.create(
                        user=request.user,
                        address=form.cleaned_data['address'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        zipcode=form.cleaned_data['zipcode']
                    )
                else:
                    shipping_address_id = request.POST.get('selected_address')
                    if shipping_address_id:
                        shipping_address = get_object_or_404(ShippingAddress, id=shipping_address_id, user=request.user)
                
                # Update order with address and receipt
                new_order.shipping_address = shipping_address
                if 'receipt' in request.FILES:
                    new_order.receipt = request.FILES['receipt']
                new_order.save()
                
                # Clear session
                if 'checkout_items' in request.session:
                    del request.session['checkout_items']
                
                # Redirect to confirmation with new order
                print(f"Redirecting to order_confirmation with order_id: {new_order.id}")  # Debug
                return redirect('store:order_confirmation', order_id=new_order.id)
        
        else:
            form = CheckoutForm()
        
        return render(request, 'store/checkout.html', {
            'order': order,
            'selected_items': selected_items,
            'selected_items_count': selected_items.count(),
            'subtotal': subtotal,
            'total': total,
            'shipping_fee': shipping,
            'form': form,
            'qr_code_url': '/media/qr_code/qrezlyn.jpg',
            'saved_addresses': saved_addresses,
        })
        
    except Exception as e:
        messages.error(request, f"Checkout error: {str(e)}")
        return redirect('store:cart')

@login_required
def checkout_selected(request):
    if request.method == 'POST':
        try:
            selected_item_ids = [int(id) for id in request.POST.getlist('selected_items') if id.isdigit()]
            
            if not selected_item_ids:
                messages.error(request, "Please select at least one item to checkout")
                return redirect('store:cart')
                
            order = Order.objects.filter(user=request.user, complete=False).first()
            
            if not order:
                messages.error(request, "No active order found")
                return redirect('store:cart')
            
            # Verify all selected items belong to this order
            valid_items = order.orderitem_set.filter(id__in=selected_item_ids)
            if valid_items.count() != len(selected_item_ids):
                messages.error(request, "Invalid items selected")
                return redirect('store:cart')
            
            request.session['checkout_items'] = selected_item_ids
            return redirect('store:checkout', order_id=order.id)
            
        except Exception as e:
            messages.error(request, f"Error processing selection: {str(e)}")
            return redirect('store:cart')
    
    return redirect('store:cart')


def search(request):
    query = request.GET.get('q', '')  # Ambil parameter 'q' dari URL
    results = Product.objects.filter(name__icontains=query) if query else []  # Cari produk berdasarkan nama
    return render(request, 'store/search.html', {'query': query, 'results': results})

def add_to_cart(request, product_id):
    # Fetch the product by ID
    product = get_object_or_404(Product, id=product_id)
    
    # If the user is logged in, get or create an order for the user
    if request.user.is_authenticated:
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
    else:
        # If the user is not logged in, handle guest carts (optional)
        # You can redirect to login page or handle it differently.
        return redirect('users:login')  # Assuming you have a login URL
    
    # Try to get an existing OrderItem for the product
    order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if not item_created:
        # If the item already exists in the cart, increment the quantity
        order_item.quantity += 1
        order_item.save()
    else:
        # Otherwise, set the quantity to 1 for the new item
        order_item.quantity = 1
        order_item.save()
    
    # Redirect back to the catalog page or product detail page
    return redirect('store:catalog')  # Or redirect to the product detail page

def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        order_item = get_object_or_404(
            OrderItem, 
            product__id=product_id, 
            order__user=request.user, 
            order__complete=False
            )
        order_item.delete()
        return redirect('store:cart')  # Redirect back to the cart page
    else:
        return redirect('users:login')

def increase_quantity(request, product_id):
    if request.user.is_authenticated:
        order_item = get_object_or_404(
            OrderItem,
            product__id=product_id,
            order__user=request.user,
            order__complete=False
        )
        order_item.quantity += 1
        order_item.save()
        return redirect('store:cart')
    else:
        return redirect('users:login')

def decrease_quantity(request, product_id):
    if request.user.is_authenticated:
        order_item = get_object_or_404(
            OrderItem,
            product__id=product_id,
            order__user=request.user,
            order__complete=False
        )
        if order_item.quantity >1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
        return redirect('store:cart')
    else:
        return redirect('users:login')
    


def track_order(request):
    if request.user.is_authenticated:
        # Only show complete orders (orders that have been placed)
        orders = Order.objects.filter(user=request.user, complete=True).order_by('-date_ordered')
    else:
        orders = None

    context = {
        'orders': orders,
    }
    return render(request, 'store/track_order.html', context)

def upload_receipt(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success-page')  # atau mana-mana URL
    else:
        form = PaymentForm()
    return render(request, 'checkout.html', {'form': form})

@login_required
def order_confirmation(request, order_id):
    print(f"Reached order_confirmation with order_id: {order_id}")  # Debug
    order = get_object_or_404(Order, id=order_id, user=request.user, complete=True)
    
    # Send email confirmation
    subject = f'Order Confirmation - Brew Beauty'
    message = render_to_string('store/order_confirmation_email.html', {
        'order': order,
        'shipping_address': order.shipping_address,
        'user': request.user
    })
    send_mail(subject, message, 'no-reply@brewbeauty.com', [request.user.email])

    return render(request, 'store/order_confirmation.html', {
        'order': order,
        'shipping_address': order.shipping_address,
    })

def sales_analytics(request):
    # Date range filter (default: last 30 days)
    date_range = request.GET.get('range', '30d')
    today = timezone.now()
    
    if date_range == '7d':
        start_date = today - timedelta(days=7)
    elif date_range == '30d':
        start_date = today - timedelta(days=30)
    elif date_range == '90d':
        start_date = today - timedelta(days=90)
    else:  # Custom range (implement as needed)
        start_date = today - timedelta(days=30)

    # Total Revenue & Orders
    orders = Order.objects.filter(date_ordered__gte=start_date, complete=True)
    total_revenue = orders.aggregate(total=Sum('orderitem__product__price'))['total'] or 0
    total_orders = orders.count()

    # Average Order Value (AOV)
    aov = total_revenue / total_orders if total_orders > 0 else 0

    # Sales Growth (%)
    prev_period_revenue = Order.objects.filter(
        date_ordered__gte=start_date - timedelta(days=30),
        date_ordered__lt=start_date,
        complete=True
    ).aggregate(total=Sum('orderitem__product__price'))['total'] or 0
    sales_growth = ((total_revenue - prev_period_revenue) / prev_period_revenue * 100) if prev_period_revenue > 0 else 0

    # Top/Bottom Selling Products
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity'),
        total_revenue=Sum(F('orderitem__quantity') * F('price'))
    ).order_by('-total_revenue')[:5]  # Top 5

    worst_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by('total_sold')[:5]  # Worst 5

    # Stock Analysis
    low_stock = Product.objects.filter(quantity__lt=F('min_stock'))
    out_of_stock = Product.objects.filter(quantity=0)

    context = {
        'date_range': date_range,
        'total_revenue': total_revenue,
        'total_orders': total_orders,
        'aov': aov,
        'sales_growth': sales_growth,
        'top_products': top_products,
        'worst_products': worst_products,
        'low_stock': low_stock,
        'out_of_stock': out_of_stock,
    }
    return render(request, 'dashboard/generatereports.html', context)