from django.urls import path, include
from . import views

app_name = 'subject'

urlpatterns = [
    path('', include('rest_framework.urls', namespace='rest_framework_category')),
    path('findSubject/', views.findSubject),
]