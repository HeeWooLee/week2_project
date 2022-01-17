# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import get_user_model

# # Create your views here.
User = get_user_model()
def index(request):
    users= User.objects.exclude(username=request.user.username)
    return render(request, 'index.html', context={'users':users})

def chatPage(request):
    users= User.objects.exclude(username=request.user.username)
    return render(request, 'main_chat.html', context={'users':users})
