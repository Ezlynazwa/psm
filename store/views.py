from django.shortcuts import render, redirect
from .models import Product, Cart
from django.contrib.auth.decorators import login_required


def product_catalog(request):
    products = Product.objects.all()
    return render(request, 'product_catalog.html', {'products': products})

def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    quantity = int(request.POST['quantity'])

    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart_view')

def homepage(request):
    products = Product.objects.all()
    return render(request, 'ecommerce/homepage.html', {'products': products})