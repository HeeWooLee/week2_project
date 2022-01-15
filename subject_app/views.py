from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from .serializer import SubjectSerializer
from .models import Subject
# Create your views here
class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer