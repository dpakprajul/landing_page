from django.db import models

# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)