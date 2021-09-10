from django.db import models

class SavePost(models.Model):
    user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
