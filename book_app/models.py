from ast import mod
from django.db import models
from accounts.models import User

# Create your models here.


class BookDetail(models.Model):
    title = models.TextField()
    image = models.TextField()
    author = models.TextField()
    publisher = models.TextField()
    pubdate = models.TextField()
    def __str__(self):        
        return self.title

class LikedBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_detail = models.ForeignKey(BookDetail, on_delete=models.CASCADE)
    # what to fill in 
    def __str__(self):
        return self.user.username + '/' + self.book_detail.title

    @property
    def user_name(self):
        return self.user.username
