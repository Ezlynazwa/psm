from django.contrib import admin

from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'variation_code','category', 'price', 'quantity')
    search_fields = ('name','variation_code')
    list_filter = ('updated_at', 'category')
    list_per_page = 20

