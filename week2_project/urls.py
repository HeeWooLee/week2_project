"""week2_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import book_app
from rest_framework import routers
# user made views 
# from user_app import views as user_views
from book_app import views as book_views
from subjects import views as subject_views
# from chat.views import index, chatPage

router = routers.DefaultRouter()
router.register(r'subjects', subject_views.SubjectViewSet, basename='subject')
router.register(r'bookdetail', book_views.BookDetailViewSet, basename='bookdetail')
router.register(r'likedbook', book_views.LikedBookViewSet, basename='likedbook')

urlpatterns = [
    # path('rest-auth/password/reset/', include('rest_auth')),
    path('admin/', admin.site.urls),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('accounts/', include('allauth.urls')),
    path('subjects/', include('subjects.urls')),
    path('streams/', include('streams.urls')),
    path('book/', include('book_app.urls')),
    # path('', include(router.urls)),

    # chat
    # path('', index, name='home'),
    # path('chat/', chatPage, name='chat')

]
