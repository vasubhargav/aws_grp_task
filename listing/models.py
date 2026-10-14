from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
class Listing(models.Model):
    FURNISHING_CHOICES = [
        ('Furnished', 'Furnished'),
        ('Semi-furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    TENANT_CHOICES = [
        ('family', 'Family'),
        ('bachelor', 'Bachelor'),
        ('any', 'Any'),
    ]
    PRICE_LABEL_CHOICES = [
        ('Good', 'Good deal'),
        ('Fair', 'Fair price'),
        ('Over', 'Overpriced'),
    ]
    #bylandload
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    bhk = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    size_sqft = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    floor = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    bathrooms = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    furnishing_status = models.CharField(max_length=50, choices=FURNISHING_CHOICES)
    tenant_preference = models.CharField(max_length=50, choices=TENANT_CHOICES)
    asking_rent = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
    phone_no = PhoneNumberField(unique=True,null=True)

    #Pratiksha add the predictd 
    predicted_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_label = models.CharField(max_length=50, choices=PRICE_LABEL_CHOICES, null=True, blank=True)
    price_gap_pct = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_unusual_price = models.BooleanField(default=False)
    #normal fields by landlord 
    is_active = models.BooleanField(default=True)
    image = models.URLField(max_length=100,blank=True,null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['city'])]

    def __str__(self):
        return f"{self.title} ({self.city})"


class SavedListing(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_listings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-saved_at']
        constraints = [
            models.UniqueConstraint(fields=['user', 'listing'], name='unique_user_listing_save'),
        ]

    def __str__(self):
        return f"{self.user.username} saved {self.listing.title}"
