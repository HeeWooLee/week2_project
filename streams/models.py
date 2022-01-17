from asyncio import streams
from distutils.text_file import TextFile
from django.db import models
from accounts.models import *

# Create your models here.
class Stream (models.Model):
    LIVE = 'LI'
    TERMINATED = 'TE'
    UPCOMING = 'UP'
    STATUS_CHOICES = [
        (LIVE, 'live'),
        (TERMINATED, 'terminated'),
        (UPCOMING, 'upcoming'),
    ]
    title = models.TextField()
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    startTime = models.TextField()
    endTime = models.TextField()
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=UPCOMING,
    )

    def __str__(self):
        return "{0} {1}".format(self.id, self.title)


class isLikedStream(models.Model):
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):  
        return self.stream.title + '/' + self.user.username