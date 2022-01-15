from pickle import TRUE
from django.shortcuts import render
from json import loads 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from django.http import JsonResponse
from .serializer import SubjectSerializer
from .models import Subject
# Create your views here
class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

def findSubject(request):
    if request.method == 'POST':
        dictQuery = loads(request.body.decode('utf-8'))
        query = dictQuery['subject']
        print(query)
        response = Subject.objects.filter(subject__startswith=query)
        response = list(response.values_list("subject", flat=True))
        print(response)
        # list = []
        # for obj in response:
        #     dict = {}
        #     dict['subject'] = obj.subject
        #     list.append(dict)
        # return JsonResponse(list, safe=False)
        return JsonResponse(response, safe=False)
