from rest_framework import serializers
from .models import booking

class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = booking
        fields = '__all__'
        read_only_fields = ['tenant', 'status', 'created_at', 'decided_at']
