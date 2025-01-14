from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, ShippingAddress
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Homepage view
def homepage(request):
    products = Product.objects.all()  # Fetch all products for the homepage
    return render(request, 'store/homepage.html', {'products': products})

# Catalog page view
def catalog(request):
    products = Product.objects.all()  # Fetch all products for the catalog
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

    return render(request, 'store/view_product.html', {'product': product})
# Cart page view
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, complete=False)
    items = order.orderitem_set.all()  # Get all order items for the current cart
    total = order.get_cart_total  # Get total price of items in the cart
    cart_items = order.get_cart_items  # Get total number of items in the cart
    return render(request, 'store/cart.html', {'items': items, 'total': total, 'cart_items': cart_items})

@login_required
def checkout(request):
    # Retrieve the current user's order
    order = Order.objects.filter(user=request.user, complete=False).first()
    if not order:
        # Redirect if no order exists
        return redirect('cart')

    # Handle shipping address form submission
    if request.method == 'POST':
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']
        
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
        return redirect('order_confirmation')

    # Calculate total cart value and number of items
    cart_total = order.get_cart_total()
    cart_items = order.get_cart_items()

    return render(request, 'store/checkout.html', {
        'order': order,
        'cart_total': cart_total,
        'cart_items': cart_items
    })