from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Tweet (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    # likes = models.IntegerField(default=0)
    # parent_tweet = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)