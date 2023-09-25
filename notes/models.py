from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):


    # Priority choices
    PRIORITY_CHOICES = (
        ('High', 'high'),
        ('Medium', 'medium'),
        ('Low', 'low'),
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    number = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='Low')
    edited = models.DateTimeField(auto_now=True)  # This field will automatically update to the current date and time when the note is edited
   
   
