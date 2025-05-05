from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('homeadmin/', views.homeadmin, name='homeadmin'),
    path('manageusers/', views.manageusers, name='manageusers'),
    path('manageproducts/', views.manageproducts, name= 'manageproducts' ),
    path('generatereports/', views.generatereport, name='generatereports'), 
    path('addstaff/', views.addstaff, name='addstaff'),  
    path('addadmin/', views.addadmin, name='addadmin'),  


    
]