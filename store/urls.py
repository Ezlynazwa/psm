from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('catalog/', views.catalog, name='catalog'),  # Catalog page URL
    path('product/<int:product_id>/', views.view_product, name='view_product'),  # View Product page URL
    path('cart/', views.cart, name='cart'),  # Cart page URL
    path('cart/checkout-selected/', views.checkout_selected, name='checkout_selected'),
    path('checkout/<int:order_id>/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),    
    path('track-order/', views.track_order, name='track_order'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

]
