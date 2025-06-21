from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('homeadmin/', views.homeadmin, name='homeadmin'),
    path('homestaff/', views.homestaff, name='homestaff'),
    path('manageusers/', views.manageusers, name='manageusers'),
    path('manageproducts/', views.manageproducts, name= 'manageproducts' ),
    path('menambahproduk/', views.menambahproduk, name='menambahproduk'),
    path('editproduct/<int:pk>/', views.edit_product, name='edit_product'),
    path('deleteproduct/<int:pk>/', views.delete_product, name='delete_product'),
    path('addstaff/', views.addstaff, name='addstaff'),  
    path('addadmin/', views.addadmin, name='addadmin'), 
    path('staffproduct/', views.staffviewproducts, name='staffproduct'),
    path('manageorder/', views.manageorder, name='manageorder'),
    path('order/<int:id>/', views.orderdetail, name='orderdetail'), 
    path('report/', views.sales_report, name='sales_report'),
    path('report/export/<str:format_type>/', views.export_report, name='export_report'),
    path('product/<int:pk>/view/', views.view_product, name='view_product'),
    path('staff/viewproduct/<int:pk>/', views.staff_view_product, name='staff_view_product'),


    
]