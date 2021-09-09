from django.db import models
from django.contrib.auth.models import User


class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.OneToOneField(User, on_delete=models.CASCADE)

