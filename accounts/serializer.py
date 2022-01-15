from rest_framework.authtoken.models import Token
from rest_framework import serializers
from .models import User

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'