from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.
@staff_member_required
def homeadmin(request):
    return render(request,'dashboard/homeadmin.html')

@staff_member_required
def manage_staffs(request):
    return render(request, 'dashboard/manageusers.html')

@staff_member_required
def manage_products(request):
    return render(request, 'dashboard/manageproducts.html')

@staff_member_required
def generate_report(request):
    return render(request, 'dashboard/generatereports.html')
