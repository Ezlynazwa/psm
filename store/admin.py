from django.contrib import admin
from users.models import User
from .models import Product
from django.utils.safestring import mark_safe
from django import forms
from .models import Order, OrderItem



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'category']
    list_filter = ['category', 'skin_type', 'skin_condition']
    ordering = ['name']
    list_per_page = 10

class ProductAdminForm(forms.ModelForm):
    class Meta:
       model = Product
       fields = '__all__'

    def photo_display(self, obj):
     if obj.images:
        return mark_safe(f'<img src="{obj.images.url}" width="50" height="50" />')
     return "No Photo"
    photo_display.allow_tags = True
    photo_display.short_description = 'Photo'
    print(Product.images)  # Debugging path fail


admin.site.register(Product, ProductAdmin)

