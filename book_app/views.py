
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

def addBook(request):
    if request.method == 'POST':
        dictQuery = loads(request.body.decode('utf-8'))
        title = dictQuery['title']
        image = dictQuery['image'] 
        author = dictQuery['author'] 
        publisher = dictQuery['publisher'] 
        pubdate = dictQuery['pubdate'] 
        if not BookDetail.objects.filter(
            title=title
        ).filter(
            image=image
        ).filter(
            author=author
        ).filter(
            publisher=publisher
        ).filter(
            pubdate=pubdate
        ).exists():
            BookDetail.objects.create(title=title,
                image=image, author=author,
                publisher=publisher,
                pubdate=pubdate)
            return JsonResponse("book created", safe=False)
        else:
            return JsonResponse("book already exists", safe=False)
        
def isBookLiked(request):
    if request.method == 'POST':
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        dictQuery = loads(request.body.decode('utf-8'))
        title = dictQuery['title']

        dict = {}
        dict['isLiked'] = True
        if LikedBook.objects.filter(user__id__exact=usrid).filter(book_detail__title__exact=title):
            print(dict)
            dict['isLiked'] = True
            return JsonResponse(dict, safe=False)
        else:
            print(dict)
            dict['isLiked'] = False
            return JsonResponse(dict, safe=False) 


def LikedBookList(request):
    # get list
    if request.method == 'GET':
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

    # delete
    if request.method == 'DELETE':
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

    # add
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

        requestBookDetail = BookDetail.objects.filter(
            title=title
        ).filter(
            image=image
        ).filter(
            author=author
        ).filter(
            publisher=publisher
        ).filter(
            pubdate=pubdate
        )
        if not requestBookDetail:
            bookDetail = BookDetail.objects.create(title=title,
                image=image, author=author,
                publisher=publisher,
                pubdate=pubdate)
        else:
            bookDetail = BookDetail.objects.get(title=title,
                image=image, author=author,
                publisher=publisher,
                pubdate=pubdate)
            if LikedBook.objects.filter(book_detail__id__exact=bookDetail.id).filter(user__id__exact=usrid):
                return JsonResponse("already liked", safe=False)
        print("bookdetail")
        print(bookDetail)
        likedBook = LikedBook.objects.create(user=user,book_detail=bookDetail)
        print("likedBook")
        print(likedBook)
        return JsonResponse(data={"liked book add success":"ok"}, safe=False)
# .filter(book_detail__title__exact=title).first()

# liked list handled


