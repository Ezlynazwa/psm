from django.db import models
from django.conf import settings
from store.models import Product, ProductVariation
from users.models import User, CustomerProfile

class SkinProfile(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE, related_name='skin_profile')
    
    # Skin Type (Required)
    skin_type = models.CharField(
        max_length=20,
        choices=Product.SKIN_TYPES,
        default='normal'
    )
    
    # Skin Concerns (Multiple)
    concerns = models.CharField(
        max_length=200,
        blank=True,
        help_text="Comma-separated (e.g., Acne-Prone, Sensitive)"
    )
    
    # Undertone & Sensitivity
    undertone = models.CharField(
        max_length=20,
        choices=ProductVariation.SKIN_TONES,
        blank=True
    )
    sensitivity = models.CharField(
        max_length=10,
        choices=Product.SENSITIVITY_LEVELS,
        default='medium'
    )
    
    # Texture & Finishing Preferences
    texture_preference = models.CharField(
        max_length=20,
        choices=Product.TEXTURE,
        blank=True
    )
    finish_preference = models.CharField(
        max_length=20,
        choices=Product.FINISHING,
        blank=True
    )
    
    def __str__(self):
        return f"{self.customer.user.username}'s Skin Profile"