from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'), 
]
