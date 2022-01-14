from django.db import models

# Create your models here.
class User(models.Model):
    userName = models.TextField(unique=True)
    passWord = models.TextField()
    def __str__(self):
        return self.userName + " " + self.passWord