from django.db import models

class WikiData(models.Model):
    title = models.CharField(max_length=200)
    date = models.CharField(max_length=20)
    description = models.TextField()
