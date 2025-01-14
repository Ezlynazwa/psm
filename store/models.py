from django.db import models
from django.contrib.auth.models import User


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
        ('Sangat Cerah','Sangat Cerah'),
        ('Cerah','Cerah'),
        ('Terang','Terang'),
        ('Sederhana','Sederhana'),
        ('Sawo Matang','Sawo Matang'),
        ('Gelap','Gelap'),
        ('Sangat Gelap','Sangat Gelap'),
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
    category = models.CharField(max_length=100, blank=True, null=True)
    variation_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPES, blank=True, null=True)
    skin_condition = models.CharField(max_length=20, choices=SKIN_CONDITIONS, blank=True, null=True)
    skin_tone = models.CharField(max_length=20, choices=SKIN_TONES, blank=True, null=True)
    surface_tones = models.CharField(max_length=20, choices=SURFACE_TONES, blank=True, null=True)
    skin_texture = models.CharField(max_length=20, choices=SKIN_TEXTURE_CHOICES, blank=True, null=True)
    sensitivity_level = models.CharField(max_length=10, choices=SENSITIVITY_LEVELS, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


    def __str__(self):
        return f'{self.user.username} - {self.product.name} ({self.quantity})'
