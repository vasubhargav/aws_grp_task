from django.db import models
from django.conf import settings
from listing.models import Listing

class booking(models.Model):
    STATUS_CHOICES = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tenant_bookings', on_delete=models.CASCADE)
    property = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    message = models.TextField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    decided_at = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Return a readable booking description
    def __str__(self):
        return f"{self.tenant.username} booked {self.property}"
