from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_required



# Create your views here.
@staff_required
def homeadmin(request):
    return render(request,'dashbord/homeadmin.html')

@staff_required
def manage_staffs(request):
    return render(request, 'dashboard/managestaffs.html')

@staff_required
def manage_products(request):
    return render(request, 'dashboard/manageproducts.html')
