from urllib import response
from django.shortcuts import render
from json import loads
from django.http import JsonResponse
from django.core.exceptions import SuspiciousOperation
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from .serializer import *
from .models import *
# Create your views here.

class StreamViewSet(ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

def onlyLive(request):
    if request.method == 'GET':
        streamList = Stream.objects.filter(status__exact='LI')
        responseList =[]
        for obj in streamList:
            dict = {}
            dict['id'] = obj.id
            dict['title'] = obj.title
            dict['host'] = obj.host.username
            dict['startTime'] = obj.startTime
            dict['endTime'] = obj.endTime
            dict['status'] = obj.status
            responseList.append(dict)
        return JsonResponse(responseList, safe = False)


def myStream(request):
    # request header
    token_string =request.headers['Key']
    userid = Token.objects.get(key=token_string).user_id
    if request.method == 'GET':
        mystream = Stream.objects.filter(host__id__exact=userid)
        print(mystream)
        totalDict ={}
        statList = ['LI', 'UP', 'TE']
        for stat in statList: 
            streamList = mystream.filter(status__exact=stat).order_by('id').reverse()
            tempList =[]
            for obj in streamList:
                dict = {}
                dict['id'] = obj.id
                dict['title'] = obj.title
                dict['host'] = obj.host.username
                dict['startTime'] = obj.startTime
                dict['endTime'] = obj.endTime
                dict['status'] = obj.status
                tempList.append(dict)
            totalDict[stat]=tempList

        return JsonResponse(totalDict, safe = False)

def addStream(request):
    # request header
    token_string =request.headers['Key']
    userid = Token.objects.get(key=token_string).user_id

    # add stream
    if request.method == 'POST':
        #request body
        dictQuery = loads(request.body.decode('utf-8'))
        title = dictQuery['title'] 
        startTime = dictQuery['startTime'] 
        endTime = dictQuery['endTime']

        user = User.objects.get(id__exact=userid)
        newStream = Stream.objects.create(host=user, title=title, startTime=startTime, endTime=endTime)
        if newStream:
            return JsonResponse(newStream.id, safe=False)
        else: 
            raise SuspiciousOperation("cannot make new stream")

    # get stream list 
    if request.method == 'GET':
        totalDict ={}
        statList = ['LI', 'UP', 'TE']
        for stat in statList: 
            streamList = Stream.objects.filter(status__exact=stat)
            tempList =[]
            for obj in streamList:
                dict = {}
                dict['id'] = obj.id
                dict['title'] = obj.title
                dict['host'] = obj.host.username
                dict['startTime'] = obj.startTime
                dict['endTime'] = obj.endTime
                dict['status'] = obj.status
                tempList.append(dict)
            totalDict[stat]=tempList

        return JsonResponse(totalDict, safe = False)

def likedStream(request):
    # request header
    token_string =request.headers['Key']
    usrid = Token.objects.get(key=token_string).user_id
    #request body
    dictQuery = loads(request.body.decode('utf-8'))
    streamid = dictQuery['streamId']

    # unlike and like toggle 
    if request.method == 'POST':
        stream = isLikedStream.objects.filter(user__id__exact=usrid).filter(stream__id__exact=streamid)

        # toggle 
        if stream:
            stream.delete()
            return JsonResponse("stream not liked anymore", safe=False)
        else: 
            streamObj = Stream.objects.get(id__exact=streamid)
            userObj = User.objects.get(id__exact=usrid)
            isLikedStream.objects.create(stream=streamObj, user=userObj)
            return JsonResponse("liked stream added", safe=False)
    
    # liked stream list 
    if request.method == 'GET':
        list = []
        stream = isLikedStream.objects.filter(user__id__exact=usrid).order_by('id').reverse()
        for obj in stream:
            dict = {}
            dict['id'] = obj.id
            dict['title'] = obj.stream.title
            dict['host'] = obj.stream.host.username
            dict['startTime'] = obj.stream.startTime
            dict['endTime'] = obj.stream.endTime
            dict['status'] = obj.stream.status
            list.append(dict)

        return JsonResponse(list, safe = False)

def changeStatus(request):
    # request header
    token_string =request.headers['Key']
    usrid = Token.objects.get(key=token_string).user_id
    #request body
    dictQuery = loads(request.body.decode('utf-8'))
    streamid = dictQuery['streamId']
    stat = dictQuery['status']
    print(stat)
    statList = ['LI', 'UP', 'TE']
    if request.method == 'POST':
        stream = Stream.objects.get(id__exact=streamid)
        if stat not in statList:
            raise SuspiciousOperation("not valid status request")

        # if host is requested stream host 
        if stream.host.id == usrid:
            stream.status = stat
            stream.save()
            print (stream.id)
            return JsonResponse(stream.id, safe=False)
        else:
            raise SuspiciousOperation("current user is not a stream host")
