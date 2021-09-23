from django.db import models

class Comment(models.Model):
    content = models.CharField( max_length=250)
    timestamp = models.IntegerField()
    author = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)

    def __str__(self):
        return self.content