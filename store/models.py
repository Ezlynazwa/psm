from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Product(models.Model):
    SKIN_TYPES = [
        ('all', 'All Skin Types'),
        ('oily', 'Oily'),
        ('dry', 'Dry'),
        ('combination', 'Combination'),
        ('normal', 'Normal'),
        ('sensitive', 'Sensitive'),
    ]

    TEXTURE = [
        ('liquid', 'Liquid'),
        ('cream', 'Cream'),
        ('powder', 'Powder'),
        ('stick', 'Stick'),
        ('gel', 'Gel'),
    ]
    
    SKIN_CONDITIONS = [
        ('Acne-Prone', 'Acne-Prone'),
        ('Sensitive', 'Sensitive'),
        ('Dehydrated', 'Dehydrated'),
    ]
    SENSITIVITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    SKIN_TEXTURE = [
        ('Licin', 'Licin'),
        ('Kasar', 'Kasar'),
        ('Pori Besar', 'Pori Besar'),
        ('Berparut', 'Berparut'),
        ('Berkedut', 'Berkedut'),
    ]

    FINISHING = [
        ('matte', 'Matte'),
        ('dewy', 'Dewy'),
        ('satin', 'Satin'),
        ('glitter', 'Glitter'),
    ]

    COVERAGE_LEVEL=[
            ('light', 'Light'),
            ('medium', 'Medium'),
            ('full', 'Full'),
            ('buildable', 'Buildable')
        ]
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, default='Brand')
    size = models.CharField(max_length=20, help_text="e.g., 30ml, 50g", default='Size')
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=100)
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, blank=True, null=True)
    suitable_for = models.CharField(max_length=20, choices=SKIN_TYPES, default='all')
    finish = models.CharField(max_length=20, choices=FINISHING, blank=True)
    texture = models.CharField(max_length=20, choices=TEXTURE, blank=True, null=True)
    skin_condition = models.CharField(max_length=20, choices=SKIN_CONDITIONS, blank=True, null=True)
    skin_texture = models.CharField(max_length=20, choices=SKIN_TEXTURE, blank=True, null=True)
    sensitivity_level = models.CharField(max_length=10, choices=SENSITIVITY_LEVELS, blank=True, null=True)
    is_vegan = models.BooleanField(default=False, blank=True, null=True)
    is_cruelty_free = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    category = models.CharField(max_length=20, null=True, blank=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    long_last = models.BooleanField(default=False, verbose_name="Tahan Lama?", blank=True, null=True)
    waterproof = models.BooleanField(default=False, blank=True, null=True)
    spf = models.IntegerField( null=True, blank=True)
    coverage = models.CharField(max_length=20, choices=COVERAGE_LEVEL, blank=True, null=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_image/')
    
class ProductVariation(models.Model):

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
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_code = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    skin_tone = models.CharField(max_length=20, choices=SKIN_TONES, blank=True, null=True)
    surface_tones = models.CharField(max_length=20, choices=SURFACE_TONES, blank=True, null=True)

    
    def __str__(self):
        return f'{self.product.name} ({self.variation_code})'

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
@receiver([post_save, post_delete], sender=ProductVariation)
def update_product_quantity(sender, instance, **kwargs):
    product = instance.product
    total_quantity = product.variations.aggregate(
        total=models.Sum('quantity')
    )['total'] or 0
    product.quantity = total_quantity
    product.save()


class Order(models.Model): 
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified - Payment Confirmed'),
        ('preparing', 'Preparing Order'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    parcel_image = models.ImageField(upload_to='parcel_images/', blank=True, null=True)
    status_updated = models.DateTimeField(auto_now=True)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
)

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate order ID if not set
            self.id = f"ORD-{str(self.id).zfill(6)}"
        if self.transaction_id is None:
            self.transaction_id = f"TRANS-{self.id or ''}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id or str(self.id)

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
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        if self.product:
            return self.product.price * self.quantity
        return 0
    
    def __str__(self):
        return f"{self.product.name if self.product else 'Deleted Product'} - {self.quantity}"
    
#model for inventory age tracking
class InventoryLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock_in = models.PositiveIntegerField()
    stock_out = models.PositiveIntegerField()
    date_logged = models.DateField(auto_now_add=True)

class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='shipping_addresses')
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

class Payment(models.Model):
        receipt = models.FileField(upload_to='payment_receipts/', null=True, blank=True)
        order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment', null=True, blank=True)
        
        def __str__(self):
            return f"Payment for {self.order.order_id}"
