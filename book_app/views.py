from json import loads 
from urllib import response
from django.http import JsonResponse
from django.http.response import HttpResponse
from django.shortcuts import render
from book_app.models import LikedBook, BookDetail
from accounts.models import User
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from .serializer import LikedBookSerializer, BookDetailSerializer
from rest_framework.authtoken.models import Token


def checkToken(request):
    if request.method == 'POST':
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id
        

# Create your views here.
class BookDetailViewSet(ModelViewSet):
    queryset= BookDetail.objects.all()
    serializer_class = BookDetailSerializer
    search_fields = ['user__username']

class LikedBookViewSet(ModelViewSet):
    queryset= LikedBook.objects.all()
    serializer_class = LikedBookSerializer

def LikedBookList(request):
    if request.method == 'POST':
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id
        
        print(usrid)
        list = []
        response = LikedBook.objects.filter(user__id__exact=usrid)
    
        for obj in response:
            dict = {}
            dict['title'] = obj.book_detail.title
            dict['image'] = obj.book_detail.image
            dict['author'] = obj.book_detail.author
            dict['publisher'] = obj.book_detail.publisher
            dict['pubdate'] = obj.book_detail.pubdate
            list.append(dict)
        return JsonResponse(list, safe=False)

# .filter(book_detail__title__exact=title).first()
def deleteLikedBook(request):
    if request.method == 'POST':
        dictQuery = loads(request.body.decode('utf-8'))
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id
        
        title = dictQuery['title']
        print(usrid)
        print(title)
        model = LikedBook.objects.filter(user__id__exact=usrid).filter(book_detail__title__exact=title)
        print(model)
        model.delete()
        if not model:
            return JsonResponse(data={"delete success":"ok"}, safe=False)
        else: 
            return JsonResponse(data={"delete fail":"not ok"}, safe=False)

def addLikedBook(request):
    if request.method == 'POST':
        dictQuery = loads(request.body.decode('utf-8'))
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id
        # print(dictQuery)
        # usr = dictQuery['username']
        # print(usr)
        title = dictQuery['title']
        image = dictQuery['image'] 
        author = dictQuery['author'] 
        publisher = dictQuery['publisher'] 
        pubdate = dictQuery['pubdate'] 
        print(title)
        # if not exist, add
        user = User.objects.get(id__exact=usrid)
        print("user")
        print(user)
        if not LikedBook.objects.filter(
            book_detail__title=title
        ).filter(
            book_detail__image=image
        ).filter(
            book_detail__author=author
        ).filter(
            book_detail__publisher=publisher
        ).filter(
            book_detail__pubdate=pubdate
        ).exists():
            bookDetail = BookDetail.objects.create(title=title,
                image=image, author=author,
                publisher=publisher,
                pubdate=pubdate)
        else:
            bookDetail = BookDetail.objects.get(title=title,
                image=image, author=author,
                publisher=publisher,
                pubdate=pubdate)
        print("bookdetail")
        print(bookDetail)
        likedBook = LikedBook.objects.create(user=user,book_detail=bookDetail)
        print("likedBook")
        print(likedBook)
        return JsonResponse(data={"add success":"ok"}, safe=False)
# liked list handled


