from django.contrib import admin
from users.models import User
from .models import Product
from django.utils.safestring import mark_safe


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'category']
    list_filter = ['category', 'skin_type', 'skin_condition']
    ordering = ['name']
    list_per_page = 10

    def photo_display(self, obj):
     if obj.photo:
        return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
     return "No Photo"
    photo_display.allow_tags = True
    photo_display.short_description = 'Photo'

admin.site.register(User)
