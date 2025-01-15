from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.contrib import admin


class Product(models.Model):
    SKIN_TYPES = [
        ('Oily', 'Oily'),
        ('Dry', 'Dry'),
        ('Combination', 'Combination'),
        ('Normal', 'Normal'),
    ]
    SKIN_CONDITIONS = [
        ('Acne-Prone', 'Acne-Prone'),
        ('Sensitive', 'Sensitive'),
        ('Dehydrated', 'Dehydrated'),
    ]
    SKIN_TONES = [
        ('Cool Undertone', 'Cool Undertone'),
        ('Warm Undertone', 'Warm Undertone'),
        ('Neutral Undertone', 'Neutral Undertone'),
    ]
    SURFACE_TONES = [
        ('Sangat Cerah', 'Sangat Cerah'),
        ('Cerah', 'Cerah'),
        ('Terang', 'Terang'),
        ('Sederhana', 'Sederhana'),
        ('Sawo Matang', 'Sawo Matang'),
        ('Gelap', 'Gelap'),
        ('Sangat Gelap', 'Sangat Gelap'),
    ]
    SENSITIVITY_LEVELS = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    SKIN_TEXTURE_CHOICES = [
        ('Licin', 'Licin'),
        ('Kasar', 'Kasar'),
        ('Pori Besar', 'Pori Besar'),
        ('Berparut', 'Berparut'),
        ('Berkedut', 'Berkedut'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=100)
    variation_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, blank=True, null=True)
    skin_condition = models.CharField(max_length=20, choices=SKIN_CONDITIONS, blank=True, null=True)
    skin_tone = models.CharField(max_length=20, choices=SKIN_TONES, blank=True, null=True)
    surface_tones = models.CharField(max_length=20, choices=SURFACE_TONES, blank=True, null=True)
    skin_texture = models.CharField(max_length=20, choices=SKIN_TEXTURE_CHOICES, blank=True, null=True)
    sensitivity_level = models.CharField(max_length=10, choices=SENSITIVITY_LEVELS, blank=True, null=True)
    images = models.ImageField(upload_to='product_image/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)  # Allow null




    def __str__(self):
        return f'{self.name} ({self.variation_code})'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])  # Corrected to call get_total method of OrderItem
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total



class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        # Multiply the product's price by the quantity to get the total for this item
        if self.product:  # Ensure the product is not None
            return self.product.price * self.quantity
        return 0  # Return 0 if no product exists



class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'quantity', 'category', 'created_at', 'updated_at']
    search_fields = ['name', 'category__name']
    list_filter = ['category', 'skin_type', 'skin_condition']
    ordering = ['name']
    list_per_page = 10

    def photo_display(self, obj):
        if obj.images:
            return mark_safe(f'<img src="{obj.images.url}" width="50" height="50" />')
        return "No Photo"
    photo_display.allow_tags = True
    photo_display.short_description = 'Photo'
