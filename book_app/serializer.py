from rest_framework import serializers
from .models import LikedBook,BookDetail
from user_app.serializer import UserSerializer

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetail
        fields = '__all__'

class LikedBookSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book_detail = BookDetailSerializer()
    class Meta:
        model = LikedBook
        fields = ('user', 'book_detail')