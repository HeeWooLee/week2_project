from django.urls import path, include
from . import views
from rest_framework import routers
from .views import LikedBookViewSet
router = routers.DefaultRouter()
router.register('Book', LikedBookViewSet)
app_name = 'book_app'

urlpatterns = [
    # path('', include(router.urls)),
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
    path('LikedBookList/', views.LikedBookList),
    path('deleteLikedBook/', views.deleteLikedBook),
    path('addLikedBook/', views.addLikedBook)
]