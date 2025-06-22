from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User, CustomerProfile

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
        ('acne', 'Acne-Prone'),
        ('sensitive', 'Sensitive'),
        ('dehydrated', 'Dehydrated'),
        ('aging', 'Aging'),
        ('redness', 'Redness'),
        ('pigmentation', 'Pigmentation'),
    ]
    SENSITIVITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    SKIN_TEXTURE = [
        ('smooth', 'Smooth'),
        ('rough', 'Rough'),
        ('large_pores', 'Large Pores'),
        ('scarred', 'Scarred'),
        ('wrinkled', 'Wrinkled'),
    ]

    FINISHING = [
        ('matte', 'Matte'),
        ('dewy', 'Dewy'),
        ('satin', 'Satin'),
        ('glitter', 'Glitter'),
    ]

    COVERAGE_LEVEL = [
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('full', 'Full'),
        ('buildable', 'Buildable'),
    ]

    # Basic Info
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, default='Brand')
    size = models.CharField(max_length=20, help_text="e.g., 30ml, 50g", default='Size')
    description = models.TextField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    detailed_description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed product benefits and features"
    )

    # Pricing & Stock
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(blank=True, null=True)
    min_stock = models.PositiveIntegerField(default=0)
    max_stock = models.PositiveIntegerField(default=100)

    # Skin‐Related Fields
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, blank=True, null=True)
    suitable_for = models.CharField(max_length=20, choices=SKIN_TYPES, default='all')
    finish = models.CharField(max_length=20, choices=FINISHING, blank=True, null=True)
    texture = models.CharField(max_length=20, choices=TEXTURE, blank=True, null=True)
    skin_condition = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Comma-separated list of conditions this product addresses"
    )
    skin_texture = models.CharField(max_length=20, choices=SKIN_TEXTURE, blank=True, null=True)
    sensitivity_level = models.CharField(max_length=10, choices=SENSITIVITY_LEVELS, blank=True, null=True)
    is_vegan = models.BooleanField(default=False, blank=True, null=True)
    is_cruelty_free = models.BooleanField(default=False, blank=True, null=True)
    is_hypoallergenic = models.BooleanField(default=False)

    # Additional Attributes
    category = models.CharField(max_length=20, null=True, blank=True)
    subcategory = models.CharField(max_length=50, blank=True, null=True)
    digital = models.BooleanField(default=False, null=True, blank=True)
    long_last = models.BooleanField(default=False, verbose_name="Long Lasting?", blank=True, null=True)
    waterproof = models.BooleanField(default=False, blank=True, null=True)
    spf = models.IntegerField(null=True, blank=True)
    coverage = models.CharField(max_length=20, choices=COVERAGE_LEVEL, blank=True, null=True)

    # Text‐search & Popularity
    tags = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated tags for search (e.g. 'hydrating,non_comedogenic')"
    )
    popularity_score = models.FloatField(
        default=0.0,
        help_text="Product popularity normalized over all in-stock items"
    )

    # -------- Change here: reference CustomerProfile directly --------
    from users.models import CustomerProfile
    recommended_for = models.ManyToManyField(
        CustomerProfile,
        through='ProductRecommendation',
        related_name='recommended_products'
    )

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    class Meta:
        ordering = ['-popularity_score', 'name']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"{self.brand} - {self.name}"

    def get_skin_conditions_list(self):
        """
        Returns a list of individual skin conditions, e.g. ['acne', 'redness'].
        """
        return [c.strip() for c in self.skin_condition.split(',')] if self.skin_condition else []

    @property
    def is_in_stock(self):
        return self.quantity > 0
    
    @property
    def total_variation_quantity(self):
        return self.variations.aggregate(total=models.Sum('quantity'))['total'] or 0

    @property
    def units_sold(self):
        from store.models import OrderItem
        return OrderItem.objects.filter(
            product=self,
            order__complete=True
        ).aggregate(total=models.Sum('quantity'))['total'] or 0


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_image/')
    

class ProductVariation(models.Model):
    SKIN_TONES = [
        ('cool', 'Cool Undertone'),
        ('warm', 'Warm Undertone'),
        ('neutral', 'Neutral Undertone'),
        ('olive', 'Olive Undertone'),
    ]
    SURFACE_TONES = [
        ('very_fair', 'Very Fair'),
        ('fair', 'Fair'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('tan', 'Tan'),
        ('dark', 'Dark'),
        ('very_dark', 'Very Dark'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_code = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    skin_tone = models.CharField(max_length=20, choices=SKIN_TONES, blank=True, null=True)
    surface_tones = models.CharField(max_length=20, choices=SURFACE_TONES, blank=True, null=True)
    hex_color = models.CharField(
        max_length=7,
        blank=True,
        null=True,
        help_text="Hex color code for display (e.g. '#F2C4A1')"
    )

    class Meta:
        unique_together = ('product', 'variation_code')
        verbose_name = "Product Variation"
        verbose_name_plural = "Product Variations"

    def __str__(self):
        return f'{self.product.name} ({self.variation_code})'

    @property
    def imageURL(self):
        try:
            return self.image.url
        except:
            return ''

    @property
    def units_sold(self):
        from store.models import OrderItem
        return OrderItem.objects.filter(variation=self, order__complete=True).aggregate(
            total=models.Sum('quantity')
        )['total'] or 0


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, null=True, blank=True, on_delete=models.SET_NULL)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'product', 'variation']

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

# Keep product.quantity in sync with sum of variation quantities
@receiver([post_save, post_delete], sender=ProductVariation)
def update_product_quantity(sender, instance, **kwargs):
    product = instance.product
    total_quantity = product.variations.aggregate(total=models.Sum('quantity'))['total'] or 0
    product.quantity = total_quantity
    product.save()



class ProductRecommendation(models.Model):
    
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    match_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        help_text="How well this product matches the customer's profile (0–1)",
    )
    reason = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short explanation (e.g., 'Content:0.8 | Rule:0.5 | Shade:Yes')",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "customer")
        ordering = ["-match_score"]
        verbose_name = "Product Recommendation"
        verbose_name_plural = "Product Recommendations"

    def __str__(self):
        return f"Reco: {self.customer.user.username} → {self.product.name} ({self.match_score:.2f})"


class Order(models.Model): 
    STATUS_CHOICES = (
        ('pending', 'Pending Verification'),
        ('verified', 'Verified - Payment Confirmed'),
        ('preparing', 'Preparing Order'),
        ('shipped', 'Shipped'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    parcel_image = models.ImageField(upload_to='parcel_images/', blank=True, null=True)
    status_updated = models.DateTimeField(auto_now=True)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    shipping_address = models.ForeignKey('ShippingAddress', on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)    

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
    variation = models.ForeignKey(ProductVariation, on_delete=models.SET_NULL, null=True, blank=True)


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

class CustomerAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)

    def __str__(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zipcode}"

class ShippingAddress(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='shipping_addresses')
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.order.id} - {self.address}, {self.city}, {self.state}, {self.zipcode}"
    
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


