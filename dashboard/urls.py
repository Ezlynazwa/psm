from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('homeadmin/', views.homeadmin, name='homeadmin'),
    path('homestaff/', views.homestaff, name='homestaff'),
    path('manageusers/', views.manageusers, name='manageusers'),
    path('manageproducts/', views.manageproducts, name= 'manageproducts' ),
    path('addproduct/', views.add_product, name='add_product'),
    path('editproduct/<int:pk>/', views.edit_product, name='edit_product'),
    path('deleteproduct/<int:pk>/', views.delete_product, name='delete_product'),
    path('generatereports/', views.generatereport, name='generatereports'), 
    path('addstaff/', views.addstaff, name='addstaff'),  
    path('addadmin/', views.addadmin, name='addadmin'), 
    path('staffproduct/', views.staffproduct, name='staffproduct'),
    path('manageorder/', views.manageorder, name='manageorder'),
    path('order/<int:id>/', views.orderdetail, name='orderdetail'), 


    
]