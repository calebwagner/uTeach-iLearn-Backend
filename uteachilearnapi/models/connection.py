from django.db import models


class Connection(models.Model):
    user = models.ForeignKey("AppUser", related_name='app_user' ,on_delete=models.CASCADE)
    profile = models.ForeignKey("AppUser", related_name='profile' ,on_delete=models.CASCADE)

