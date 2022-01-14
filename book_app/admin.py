from django.contrib import admin

# Register your models here.
from .models import BookDetail, LikedBook

admin.site.register(BookDetail)
admin.site.register(LikedBook)