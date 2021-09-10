from django.db import models


class Connection(models.Model):
    user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    profile = models.ForeignKey("AppUser", on_delete=models.CASCADE)

