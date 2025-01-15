from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, ShippingAddress
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from.forms import ProductForm
from .forms import CheckoutForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator





# Homepage view
def homepage(request):
    products = Product.objects.all()  # Fetch all products for the homepage
    return render(request, 'store/homepage.html', {'products': products})

# Catalog page view

def catalog(request):
    products = Product.objects.all()
    return render(request, 'store/catalog.html', {'products': products})

# View Product page view
def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        
        # Get or create an order for the user
        order, created = Order.objects.get_or_create(user=request.user, complete=False)
        
        # Add the item to the cart
        order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity += quantity  # Increment the quantity
        order_item.save() 
        return redirect('store:cart')  # Redirect to the cart page after adding the item

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'inventori/product_form.html', {'form': form})

    return render(request, 'store/view_product.html', {'product': product})

@login_required
def cart(request):
    try:
        # Try to get the user's order (uncompleted)
        order = Order.objects.get(user=request.user, complete=False)
    except Order.DoesNotExist:
        # If no order exists, create a new order for the user
        order = Order.objects.create(user=request.user, complete=False)

    # Calculate total cart value and number of items
    cart_total = order.get_cart_total
    cart_items = order.get_cart_items

    return render(request, 'store/cart.html', {
        'order': order,
        'cart_total': cart_total,
        'cart_items': cart_items
    })

@login_required
def checkout(request):
    # Retrieve the current user's order
    order = Order.objects.filter(user=request.user, complete=False).first()
    if not order:
        # Redirect if no order exists
        return redirect('store:cart')
    else:
        form = CheckoutForm()

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            # Create and save the shipping address
            shipping_address = ShippingAddress(
            user=request.user,
            order=order,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode
            )
            shipping_address.save()

            # Mark the order as complete
            order.complete = True
            order.save()

            # Redirect to an order confirmation page (you can create this later)
            return redirect('store:order_confirmation')

    # Calculate total cart value and number of items
    cart_total = order.get_cart_total
    cart_items = order.get_cart_items

    return render(request, 'store/checkout.html', {
        'order': order,
        'cart_total': cart_total,
        'cart_items': cart_items,
        'form': form
    })

def search(request):
    query = request.GET.get('q', '')  # Ambil parameter 'q' dari URL
    results = Product.objects.filter(name__icontains=query) if query else []  # Cari produk berdasarkan nama
    return render(request, 'store/search.html', {'query': query, 'results': results})

def view_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/view_product.html', {'product': product})

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

def remove_from_cart(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__complete=False)
        item.delete()
        return redirect('store:cart')  # Redirect back to the cart page
    else:
        return redirect('users:login')
    
@login_required
def order_confirmation(request):
    order = Order.objects.filter(user=request.user, complete=True).first()
    shipping_address = ShippingAddress.objects.filter(order=order).first()

    # Send email confirmation
    subject = f'Order Confirmation - Brew Beauty'
    message = render_to_string('store/order_confirmation_email.html', {
        'order': order,
        'shipping_address': shipping_address,
        'user': request.user
    })
    send_mail(subject, message, 'no-reply@brewbeauty.com', [request.user.email])

    return render(request, 'store/order_confirmation.html', {
        'order': order,
        'shipping_address': shipping_address,
    })