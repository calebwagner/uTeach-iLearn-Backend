from django.db import models
from django.contrib.auth.models import User


class AppUser(models.Model):
    user = models.OneToOneField(User ,on_delete=models.CASCADE)
    bio = models.CharField(max_length=50)
    image_url = models.ImageField(
        upload_to='images', height_field=None,
        width_field=None, max_length=None, null=True)
    # is_teacher = models.BooleanField()