from .models import booking
from rest_framework import serializers
class BookingSerializers(serializers.ModelSerializer):
    class Meta:
        model = booking
        fields = '__all__'
        read_only_files = [
            'tenant',
            'status',
            'created_at',
            'decided_at'
        ]