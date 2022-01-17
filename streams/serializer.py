from accounts.serializer import UserSerializer
from rest_framework import serializers
from .models import *

class StreamSerializer(serializers.ModelSerializer):
    host = UserSerializer()
    class Meta:
        model = Stream
        fields = ('title', 'host', 'startTime', 'endTime', 'status')
