from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from store.models import Product, ProductVariation


class Employee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employees', null=True, blank=True)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100, default='firstname')
    last_name = models.CharField(max_length=100, default='lastname')
    password = models.CharField(max_length=128, default='defaultpassword')
    position = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.EmailField()
    date_hired = models.DateField()
    photo = models.ImageField(upload_to='employee_photo/', blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class User(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    # Add related_name to resolve conflicts
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='loginsignup_user_permissions_set',  # Specify a unique reverse accessor name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permisions',
    )

class CustomerProfile(models.Model):
    SKIN_TYPE_CHOICES = [
        ('oily', 'Oily'),
        ('dry', 'Dry'),
        ('combination', 'Combination'),
        ('normal', 'Normal'),
        ('sensitive', 'Sensitive'),
        ('not_sure', 'Not Sure'),
    ]
    
    UNDERTONE_CHOICES = [
        ('cool', 'Cool'),
        ('warm', 'Warm'),
        ('neutral', 'Neutral'),
        ('olive', 'Olive'),
        ('not_sure', 'Not Sure'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Contact Information
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    preferred_contact_method = models.CharField(
        max_length=10,
        choices=[('email', 'Email'), ('sms', 'SMS'), ('whatsapp', 'WhatsApp')],
        default='email'
    )
    
    # Demographic Information
    gender = models.CharField(
        max_length=10,
        choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not', 'Prefer not to say')],
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='customer_profiles/', blank=True, null=True)
    
    # Skin Profile
    skin_type = models.CharField(max_length=20, choices=SKIN_TYPE_CHOICES, blank=True, null=True)
    undertone = models.CharField(max_length=10, choices=UNDERTONE_CHOICES, blank=True, null=True)
    surface_tone = models.CharField(
        max_length=20,
        choices=ProductVariation.SURFACE_TONES,
        blank=True,
        null=True
    )
    primary_skin_concerns = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Comma-separated list of skin concerns"
    )
    skin_sensitivity = models.CharField(
        max_length=10,
        choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')],
        blank=True,
        null=True
    )
    known_allergies = models.TextField(blank=True, null=True)
    
    # Product Preferences
    preferred_finish = models.CharField(
        max_length=20,
        choices=Product.FINISHING,
        blank=True,
        null=True
    )
    preferred_coverage = models.CharField(
        max_length=20,
        choices=Product.COVERAGE_LEVEL,
        blank=True,
        null=True
    )
    preferred_texture = models.CharField(
        max_length=20,
        choices=Product.TEXTURE,
        blank=True,
        null=True
    )
    ethical_preferences = models.JSONField(
        default=list,
        blank=True,
        help_text="List of ethical preferences (e.g., ['vegan', 'cruelty_free'])"
    )
    
    # Behavioral Data
    last_skin_assessment = models.DateTimeField(blank=True, null=True)
    skin_assessment_version = models.CharField(max_length=10, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_primary_concerns_list(self):
        return [concern.strip() for concern in self.primary_skin_concerns.split(',')] if self.primary_skin_concerns else []
    
    def get_ethical_preferences_list(self):
        return self.ethical_preferences if isinstance(self.ethical_preferences, list) else []
    
    class Meta:
        verbose_name = "Customer Profile"
        verbose_name_plural = "Customer Profiles"


class SkinAssessment(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='skin_assessments')
    assessment_date = models.DateTimeField(auto_now_add=True)
    
    # Skin characteristics
    hydration_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (Very Dry) to 5 (Very Hydrated)"
    )
    oiliness_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (Not Oily) to 5 (Very Oily)"
    )
    sensitivity_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (Not Sensitive) to 5 (Very Sensitive)"
    )
    acne_proneness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (Not Prone) to 5 (Very Prone)"
    )
    aging_concerns = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1 (No Concerns) to 5 (Severe Concerns)"
    )
    
    # Additional notes
    current_routine = models.TextField(blank=True, null=True)
    current_concerns = models.TextField(blank=True, null=True)
    goals = models.TextField(blank=True, null=True)
    
    # Recommendations generated
    recommendation_notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Skin Assessment for {self.customer.user.username} on {self.assessment_date}"
    
    class Meta:
        ordering = ['-assessment_date']
        verbose_name = "Skin Assessment"
        verbose_name_plural = "Skin Assessments"