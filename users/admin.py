from django.contrib import admin
from .models import Employee
from django.utils.safestring import mark_safe



class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('photo_display', 'name', 'email', 'contact', 'position', 'date_hired')
    search_fields = ['name', 'email']  # Membolehkan carian berdasarkan nama atau email
    list_filter = ('position',)
    
    
    # Function to display image in the admin panel
    def photo_display(self, obj):
     if obj.photo:
        return mark_safe(f'<img src="{obj.photo.url}" width="50" height="50" />')
     return "No Photo"
    photo_display.allow_tags = True
    photo_display.short_description = 'Photo'

admin.site.register(Employee)

