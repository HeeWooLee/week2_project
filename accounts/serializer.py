from rest_framework.authtoken.models import Token
from rest_framework import serializers

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['key']

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['key']