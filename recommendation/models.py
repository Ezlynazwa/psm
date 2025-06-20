from django.db import models
from django.conf import settings
from store.models import Product, ProductVariation
from users.models import CustomerProfile
from django.core.validators import MinValueValidator, MaxValueValidator


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
    
class SkinAssessment(models.Model):
    """
    Stores a one-time or periodic “survey” of the customer’s skin.
    Each time the user submits, we save a timestamped record.
    """
    customer = models.ForeignKey(
        'users.CustomerProfile',
        on_delete=models.CASCADE,
        related_name='skin_assessments'
    )
    assessment_date = models.DateTimeField(auto_now_add=True)

    # Numerical sliders (1–5) to capture objective measurements
    hydration_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=very dry, 5=very hydrated"
    )
    oiliness_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=very non-oily, 5=extremely oily"
    )
    sensitivity_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=not sensitive, 5=very sensitive"
    )
    acne_proneness = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=never acne, 5=always acne"
    )
    aging_concerns = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="1=no aging issues, 5=major wrinkles/aging"
    )

    surface_tone = models.CharField(
    max_length=20,
    choices=[
        ('very_fair', 'Very Fair'),
        ('fair', 'Fair'),
        ('light', 'Light'),
        ('medium', 'Medium'),
        ('tan', 'Tan'),
        ('dark', 'Dark'),
        ('very_dark', 'Very Dark'),
    ],
    blank=True,
    null=True
)

    # Free-form “multiple choice” fields capture user preferences.
    # We store them as comma-separated strings in the DB, but render them
    # in forms as checkboxes so the user can pick multiple.
    SKIN_TYPE_CHOICES = [
        ('oily', 'Oily'),
        ('dry', 'Dry'),
        ('combination', 'Combination'),
        ('normal', 'Normal'),
        ('sensitive', 'Sensitive'),
    ]
    skin_type = models.CharField(
        max_length=20,
        choices=SKIN_TYPE_CHOICES,
        help_text="Pick the one that best describes your overall skin type"
    )

    UNDERTONE_CHOICES = [
        ('cool', 'Cool'),
        ('warm', 'Warm'),
        ('neutral', 'Neutral'),
        ('olive', 'Olive'),
    ]
    undertone = models.CharField(
        max_length=20,
        choices=UNDERTONE_CHOICES,
        help_text="Your natural undertone"
    )

    # Checkboxes for general “skin concerns” (e.g. acne, redness).
    CONCERN_CHOICES = [
        ('acne', 'Acne'),
        ('aging', 'Aging'),
        ('redness', 'Redness'),
        ('dehydrated', 'Dehydrated'),
        ('sensitive', 'Sensitive'),
        ('pigmentation', 'Pigmentation'),
    ]
    concerns = models.CharField(
        max_length=255,
        blank=True,
        help_text="Comma-separated list of concerns (e.g. acne, redness)"
    )

    # If the user has a preferred finish or texture, store those too:
    FINISH_CHOICES = Product.FINISHING  # reuse from your Product model
    finish_preference = models.CharField(
        max_length=20,
        choices=FINISH_CHOICES,
        blank=True,
        null=True,
        help_text="If you prefer matte/ dewy / satin etc."
    )
    TEXTURE_CHOICES = Product.TEXTURE  # reuse from your Product model
    texture_preference = models.CharField(
        max_length=20,
        choices=TEXTURE_CHOICES,
        blank=True,
        null=True,
        help_text="If you prefer liquid/cream/ powder etc."
    )

    def __str__(self):
        return f"{self.customer.user.username} – {self.assessment_date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-assessment_date']
        verbose_name = "Skin Assessment"
        verbose_name_plural = "Skin Assessments"