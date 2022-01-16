
from xmlrpc.client import Boolean
from django.db import models
from accounts.models import User
from book_app.models import BookDetail
from django.contrib.postgres.fields import ArrayField

# Create your models here.
# comments

class Subject(models.Model):
    subject = models.TextField()

    def __str__(self):
        return self.subject

class Post(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bookDetail = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    createdAt= models.DateTimeField(auto_now=True)
    title = models.TextField()
    content = models.TextField()
    voteCount = models.IntegerField(default=0)
    commentCount = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)

    def __str__(self):        
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now=True)
    content = models.TextField()
    voteCount = models.IntegerField(default=0)
    solved = models.BooleanField(default=False)

    def __str__(self):        
        
        return  "{0} {1}".format(self.post.id, self.id)

class isLiked(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  
        return self.post.title + '/' + self.user.username

class isScrapped(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):  
        return self.post.title + '/' + self.user.username


class LikedSubject(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  
        return self.subject.subject + '/' + self.user.username


class PostVote(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField()

    def __str__(self):  
        return "{0} {1} {2}".format(self.post.id, self.user.id, self.vote)

class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.IntegerField()

    def __str__(self):  
        return  "{0} {1} {2}".format(self.comment.id, self.user.id, self.vote)