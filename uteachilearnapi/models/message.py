from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey("AppUser", related_name='sender', on_delete=models.CASCADE)
    recipient = models.ForeignKey("AppUser", related_name='recipient', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    timestamp = models.IntegerField()
    read = models.BooleanField(default=False)



