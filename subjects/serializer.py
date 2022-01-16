from accounts.serializer import UserSerializer
from rest_framework import serializers
from .models import *
from accounts.models import User
from book_app.models import BookDetail
from accounts.serializer import UserSerializer
from book_app.serializer import BookDetailSerializer

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    author = UserSerializer()
    BookDetail = BookDetailSerializer()
    class Meta:
        model = Post
        fields = ('subject', 'author', 'bookDetail', \
            'createdAt', 'title', 'content', 'voteCount', \
                'commentCount', 'solved', 'isLiked', 'isScrapped')

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    author = UserSerializer()
    class Meta:
        model = Comment
        fields = ('post', 'author', 'createdAt', 'content', \
            'voteCount', 'solved')

class LikedSubjectSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer()
    user = UserSerializer()
    class Meta:
        model = LikedSubject
        fields = ('subject','user')

class PostVoteSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserSerializer()
    class Meta:
        model = PostVote
        fields = ('post','user', 'vote')
class CommentVoteSerializer(serializers.ModelSerializer):
    comment = CommentSerializer()
    user = UserSerializer()
    class Meta:
        model = CommentVote
        fields = ('comment','user', 'vote')