from django.db import models

# Create your models here.
class Subject(models.Model):
    subject = models.TextField()
    def __str__(self):        
        return self.subject

