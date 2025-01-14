from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('catalog/', views.catalog, name='catalog'),  # Catalog page URL
    path('product/<int:product_id>/', views.view_product, name='view_product'),  # View Product page URL
    path('cart/', views.cart, name='cart'),  # Cart page URL
    path('checkout/', views.checkout, name='checkout'),
]
