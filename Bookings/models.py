from django.db import models
from django.conf import settings
from listing.models import Listing
class booking(models.Model):
    status=[
        ('pending','pending'),
        ('Approved','Apperoved'),
        ('Rejected','Rejected')
    ]
    tenant = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tenont_booking', on_delete=models.CASCADE)
    property = models.ForeignKey(Listing,on_delete=models.CASCADE ,related_name='bookings')
    message = models.TextField(max_length=250)
    created_at = models.DateField(auto_now_add=True)
    decided_at=models.DateField(null=True,blank=True)
    status = models.CharField(max_length=10,choices=status,default='pending')
    def __str__(self): 
        return f"{self.user.username} saved {self.listing.title}"
