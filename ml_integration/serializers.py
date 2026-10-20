
from rest_framework import serializers


class RentPredictionSerializer(serializers.Serializer):
    bhk = serializers.IntegerField(min_value=1)
    size = serializers.FloatField(min_value=1)
    floor = serializers.IntegerField(min_value=0)
    bathroom = serializers.IntegerField(min_value=1)

    city = serializers.CharField()
    area_type = serializers.CharField()
    furnishing_status = serializers.CharField()
    tenant_preferred = serializers.CharField()
