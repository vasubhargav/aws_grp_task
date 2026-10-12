from rest_framework import serializers
from django.contrib.auth.models import AbstractUser ,User
from .models import Account
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Account
        fields = [ 'username', 'email', 'first_name', 'last_name' , 'password', 'role', 'phone']

    def create(self, validated_data):
        user = Account.objects.create_user(**validated_data)
        return user
class loginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

