from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recipient = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    time = models.TimeField()
    read = models.BooleanField()



