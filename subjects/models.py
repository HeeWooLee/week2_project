from django.db import models

# Create your models here.
# comments
class Subject(models.Model):
    subject = models.TextField()

    def __str__(self):
        return self.subject

class Post(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    

class Comment(models.Model):

    createdAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):        
        return self.title