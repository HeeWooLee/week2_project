from rest_framework import serializers
from .models import LikedBook,BookDetail
from accounts.serializer import UserSerializer

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetail
        fields = '__all__'

    def create(self, validated_data):
        print("BookDetailSerializer Called")
        return BookDetail.objects.create(**validated_data)

class LikedBookSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book_detail = BookDetailSerializer()
    class Meta:
        model = LikedBook
        fields = ('user', 'book_detail')