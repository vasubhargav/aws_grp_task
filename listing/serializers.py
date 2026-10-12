from .models import Listing, SavedListing
from rest_framework import serializers
class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
        read_only_fields =[
            'owner',
            'predicted_rent',
            'price_label',
            'price_gap_pct',
            'is_unusual_price',
            'created_at',
            'updated_at',
        ]
class SavedListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedListing
        fields = '__all__'
        read_only_fields = ['user', 'saved_at']
        
        