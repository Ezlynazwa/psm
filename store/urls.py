from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('catalog/', views.catalog, name='catalog'),  # Catalog page URL
    path('product/<int:product_id>/', views.view_product, name='view_product'),  # View Product page URL
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('cart/', views.cart, name='cart'),  # Cart page URL
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),

]
