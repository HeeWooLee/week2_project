from distutils import core
from itertools import chain
from django.core.exceptions import SuspiciousOperation
from json import loads, dumps
from re import S
from django.forms.models import model_to_dict
from urllib import response 
from django.shortcuts import render
from django.http import JsonResponse
from book_app import serializer
from django.core import serializers as core_serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from .serializer import *
from .models import *

# Define ViewSets
class SubjectViewSet(ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

def searchSubject(request):
    if request.method == 'POST':
        dictQuery = loads(request.body.decode('utf-8'))
        subject = dictQuery['subject']

        response = Subject.objects.filter(subject__startswith=subject)
        response = list(response.values_list('subject', flat=True))
    
        return JsonResponse(response, safe=False)
    
# Subjects
def likedSubject(request):
    # add
    if request.method == 'POST':
        # get user id from request header
        token_string =request.headers['Key']
        userid = Token.objects.get(key=token_string).user_id

        dictQuery = loads(request.body.decode('utf-8'))
        subject = dictQuery['subject']

        user = User.objects.get(id__exact=userid)
        if not Subject.objects.filter(subject__exact=subject):
            subject = Subject.objects.create(subject=subject)
        else: 
            subject = Subject.objects.get(subject=subject)

        likedSubject = LikedSubject.objects.create(subject=subject, user=user)
        if likedSubject:
            return JsonResponse("success", safe=False)
        else: 
            return JsonResponse("fail", safe=False)
    
    # delete
    if request.method == 'DELETE':
        # get user id from request header
        token_string =request.headers['Key']
        userid = Token.objects.get(key=token_string).user_id

        dictQuery = loads(request.body.decode('utf-8'))
        subject = dictQuery['subject']

        subject = LikedSubject.objects.filter(user__id__exact=userid).filter(subject__subject__exact=subject)
        if subject:
            subject.delete()
            return JsonResponse("del success", safe=False)
        else: 
            return JsonResponse("no such subject", safe=False)

    # get list
    if request.method == 'GET':
        # get user id from request header
        token_string =request.headers['Key']
        userid = Token.objects.get(key=token_string).user_id

        list = []
        response = LikedSubject.objects.filter(user__id__exact=userid)
        
        for obj in response:
            list.append(obj.subject.subject)

        return JsonResponse(list, safe=False)

# Post 
def getPostList(request):
    if request.method == 'POST':
        # get response body
        dictQuery = loads(request.body.decode('utf-8'))
        subject = dictQuery['subject']
        list = []
        # get post list
        postList = Post.objects.filter(subject__subject__exact=subject)

        # calculate upvote and downvote
        print(postList)
        for obj in postList:
            dict = {}
            id = obj.id
            upVote = PostVote.objects.filter(post__id__exact=id).filter(vote=True).count()
            downVote = PostVote.objects.filter(post__id__exact=id).filter(vote=False).count()
            obj.voteCount = upVote - downVote
            obj.save()
            dict['id'] = obj.id
            dict['author'] = obj.author.username
            dict['title'] = obj.title
            dict['content'] = obj.content
            dict['voteCount'] = obj.voteCount
            dict['commentCount'] = obj.commentCount
            dict['solved'] = obj.solved
            dict['createdAt'] = obj.createdAt
            
            list.append(dict)
        return JsonResponse(list, safe = False)

def getNdelPost(request, pk):
    if request.method == 'GET':
        # get user id from request header
        token_string =request.headers['Key']
        userid = Token.objects.get(key=token_string).user_id

        # get post id from request body 
        # dictQuery = loads(request.body.decode('utf-8'))
        # postid = dictQuery['postId']
        postid = pk

        post = Post.objects.get(id__exact=postid)
        response =model_to_dict(post) 
        
        # change some attributes
        response['subject'] = post.subject.subject
        response['author'] = post.author    .username
        response['bookTitle'] = post.bookDetail.title
        del response['bookDetail']

        # check if user liked or scrapped this post 
        isliked = False
        if isLiked.objects.filter(post__id__exact=postid).filter(user__id__exact=userid):
            isliked =True
        response['isLiked'] = isliked

        # isscrapped = False
        # if isScrapped.objects.filter(post__id__exact=postid).filter(user__id__exact=userid):
        #     isscrapped =True        
        # response['isScrapped'] = isscrapped

        # return post content
        return JsonResponse(response, safe=False)
    
    if request.method == 'DELETE':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        # get response body
        # dictQuery = loads(request.body.decode('utf-8'))
        # postid = dictQuery['postId']
        postid = pk

        print("iamhere")
        delPost = Post.objects.get(id__exact=postid)
        delPostAuthor = delPost.author.id
        
        if delPostAuthor == usrid:
            delPost.delete()
            return JsonResponse("post deleted", safe=False)
        else: 
            return JsonResponse("current user is not an author", safe=False)

def addPost(request):
    if request.method == 'POST':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        print(usrid)
        # get response body
        dictQuery = loads(request.body.decode('utf-8'))
        subject = dictQuery['subject']
        title = dictQuery['title'] 
        content = dictQuery['content'] 
        bookTitle = dictQuery['bookTitle']

        # get author, book Detail, subject
        author = User.objects.get(id__exact=usrid)
        bookDetail = BookDetail.objects.get(title__exact=bookTitle)
        subjectObj = Subject.objects.get(subject__exact=subject)

        # create instance
        newPost = Post.objects.create(subject=subjectObj, author=author, bookDetail=bookDetail, \
        title=title, content=content)

        if newPost: 
            return JsonResponse(newPost.id, safe=False)
        else:
            return JsonResponse("fail to add Post", safe=False)
        
def solvedPost(request, pk):
    if request.method == 'GET':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id
        postid = pk

        solvedPost = Post.objects.get(id__exact=postid)
        solvedPostAuthor = solvedPost.author.id

        if solvedPostAuthor == usrid:
            if solvedPost.solved == False:
                solvedPost.solved = True
                print("solved")
                solvedPost.save()
                return JsonResponse("post solved", safe=False)
            else:
                solvedPost.solved = False
                print("unsolved")
                solvedPost.save()
                return JsonResponse("post unsolved  ", safe=False)
        else: 
            return JsonResponse("current user is not an author", safe=False)

def likePost(request, pk):
    if request.method == 'GET':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        postid = pk

        post = isLiked.objects.filter(user__id__exact=usrid).filter(post__id__exact=postid)
        if post:
            post.delete()
            return JsonResponse("not liked anymore", safe=False)
        else: 
            postObj = Post.objects.get(id__exact=postid)
            userObj = User.objects.get(id__exact=usrid)
            isLiked.objects.create(post=postObj, user=userObj)
            return JsonResponse("liked post added", safe=False)

def votePost(request):
    if request.method == 'POST':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id
       
        dictQuery = loads(request.body.decode('utf-8'))
        postid = dictQuery['postId']
        status = dictQuery['status']

        # get vote table
        voteObj = PostVote.objects.filter(post__id__exact=postid).filter(user__id__exact=usrid)[0]

        # if user has already voted
        if voteObj:
            # if user tries to vote same up or down vote again
            if voteObj.vote == status:
                raise SuspiciousOperation("cannot vote twice")
            postObj = Post.objects.get(id__exact=postid)
            # nullify original vote 
            voteCount = postObj.voteCount
            if status:
                postObj.voteCount = voteCount + 1
            else:
                postObj.voteCount = voteCount - 1
            voteObj.vote = status
            voteObj.save()
            voteCount = postObj.voteCount
        else:
            postObj = Post.objects.get(id__exact=postid)
            user = User.objects.get(id__exact=usrid)
            voteObj = PostVote.objects.create(post=postObj,user=user,vote=status)
            voteCount = 0
        
        print("before add", postObj.voteCount)
        # if upvote
        if status:
            postObj.voteCount = voteCount + 1
        else:
            postObj.voteCount = voteCount - 1
        print("final", postObj.voteCount)
        postObj.save()
        
        return JsonResponse("vote done", safe=False)

def searchPost(request):
    if request.method == 'POST':
        dictQuery = loads(request.body.decode('utf-8'))
        subject = dictQuery['subject']
        query = dictQuery['query']


        # search post within selected post
        posts = Post.objects.filter(subject__subject__exact=subject)
        print(posts)
        first_list = list(posts.filter(title__icontains=query).values_list('id', flat=True))
        second_list = list(posts.filter(content__icontains=query).values_list('id', flat=True))
        
        uniqueid = first_list + list(set(second_list) - set(first_list))

        postList = Post.objects.filter(id__in=uniqueid)

        response = []
        for obj in postList:
            dict = {}
            id = obj.id
            upVote = PostVote.objects.filter(post__id__exact=id).filter(vote=True).count()
            downVote = PostVote.objects.filter(post__id__exact=id).filter(vote=False).count()
            obj.voteCount = upVote - downVote
            obj.save()
            dict['id'] = obj.id
            dict['author'] = obj.author.username
            dict['title'] = obj.title
            dict['content'] = obj.content
            dict['voteCount'] = obj.voteCount
            dict['commentCount'] = obj.commentCount
            dict['solved'] = obj.solved
            dict['createdAt'] = obj.createdAt
            
            response.append(dict)
        return JsonResponse(response, safe = False)
    
# Comment 
def getCommentList(request):
    if request.method == 'POST':
        # get response body
        dictQuery = loads(request.body.decode('utf-8'))
        postid = dictQuery['postId']
        list = []
        # get comment list
        commentList = Comment.objects.filter(post__id__exact=postid)
        print(commentList)
        for obj in commentList:
            dict = {}
            id = obj.id
            upVote = CommentVote.objects.filter(comment__id__exact=id).filter(vote=True).count()
            downVote = CommentVote.objects.filter(comment__id__exact=id).filter(vote=False).count()
            obj.voteCount = upVote - downVote
            obj.save()
            dict['id'] = obj.id
            dict['author'] = obj.author.username
            dict['content'] = obj.content
            dict['voteCount'] = obj.voteCount
            dict['solved'] = obj.solved
            dict['createdAt'] = obj.createdAt
            list.append(dict)
        print(list)
        return JsonResponse(list, safe = False)

def addComment(request):
    if request.method == 'POST':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        print(usrid)
        # get response body
        dictQuery = loads(request.body.decode('utf-8'))
        post = dictQuery['postId']
        content = dictQuery['content'] 

        # get author, book Detail, subject
        author = User.objects.get(id__exact=usrid)
        postObj = Post.objects.get(id__exact=post)

        # create instance
        newComment = Comment.objects.create(post=postObj, author=author, content=content)

        if newComment: 
            commentCount = postObj.commentCount
            postObj.commentCount = commentCount +1
            postObj.save()
            return JsonResponse(newComment.id, safe=False)
        else:
            return JsonResponse("fail to add Post", safe=False)

def delComment(request, pk):
    if request.method == 'DELETE':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        commentid = pk

        delComment = Comment.objects.get(id__exact=commentid)
        delCommentAuthor = delComment.author.id
        
        if delCommentAuthor == usrid:
            post = Post.objects.get(id__exact=delComment.post.id)
            commentCount = post.commentCount
            post.commentCount= commentCount - 1
            post.save()
            delComment.delete()
            return JsonResponse("comment deleted", safe=False)
        else: 
            return JsonResponse("current user is not an author", safe=False)
        
def solvedComment(request, pk): 
    if request.method == 'GET':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        solvedComment = Comment.objects.get(id__exact=pk)
        solvedPostAuthor = solvedComment.post.author.id

        if solvedPostAuthor == usrid:
            if solvedComment.solved == False:
                solvedComment.solved = True
                postid = solvedComment.post.id
                postObj = Post.objects.get(id__exact=postid)
                postObj.solved = True
                postObj.save()
                print("solved")
                solvedComment.save()
                return JsonResponse("comment selected", safe=False)
            else:
                solvedComment.solved = False
                print("unsolved")
                solvedComment.save()
                return JsonResponse("comment unselected", safe=False)
        else: 
            return JsonResponse("current user is not an post author", safe=False)

def voteComment(request):
    if request.method == 'POST':
        # get response header
        token_string =request.headers['Key']
        usrid = Token.objects.get(key=token_string).user_id

        dictQuery = loads(request.body.decode('utf-8'))
        commentid = dictQuery['commentId']
        status = dictQuery['status']

        # get vote table
        voteObj = CommentVote.objects.filter(comment__id__exact=commentid).filter(user__id__exact=usrid)

        # if user has already voted
        if voteObj:
            # if user tries to vote same up or down vote again
            if voteObj.vote == status:
                raise SuspiciousOperation("cannot vote twice")
            commentObj = Comment.objects.get(id__exact=commentid)
            # nullify original vote 
            voteCount = commentObj.voteCount
            if status:
                commentObj.voteCount = voteCount + 1
            else:
                commentObj.voteCount = voteCount - 1
            voteCount = commentObj.voteCount
        else:
            commentObj = Comment.objects.get(id__exact=commentid)
            user = User.objects.get(id__exact=usrid)
            voteObj = CommentVote.objects.create(comment=commentObj,user=user,vote=status)
            voteCount = 0
        
        # if upvote
        if status:
            commentObj.voteCount = voteCount + 1
        else:
            commentObj.voteCount = voteCount - 1
        print("final", commentObj.voteCount)
        commentObj.save()
        
        return JsonResponse("vote done", safe=False)