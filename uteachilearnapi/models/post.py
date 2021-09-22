from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    user = models.ForeignKey("AppUser", on_delete=models.CASCADE)
    created_on = models.IntegerField()
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title