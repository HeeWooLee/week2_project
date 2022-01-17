from django.urls import path, include
from . import views
from rest_framework import routers
from .views import *

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
    
    # post
    path('post/list/', views.getPostList),
    path('post/<int:pk>', views.getNdelPost),
    path('post/', views.addPost),
    path('post/solved/<int:pk>', views.solvedPost),
    path('post/vote/', views.votePost),
    path('post/liked/<int:pk>', views.likePost),
    path('post/search/', views.searchPost),

    # comment
    path('comment/list/', views.getCommentList),
    path('comment/', views.addComment),     
    path('comment/<int:pk>', views.delComment),
    path('comment/vote/', views.voteComment),  
    path('comment/solved/<int:pk>', views.solvedComment),

    # liked subject
    path('liked/', views.likedSubject),
    
    # search
    path('search/', views.searchSubject),
]