import imp
from django.urls import path, include
from . import views
from .views import *

urlpatterns = [
    path('', views.addStream),

    # stream
    path('liked/', views.likedStream),
    path('my/', views.myStream),
    path('status/', views.changeStatus),

]
