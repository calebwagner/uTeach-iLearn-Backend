from django.db import models

class Meeting(models.Model):
    scheduler = models.ForeignKey("AppUser", related_name='scheduler' ,on_delete=models.CASCADE)
    connection = models.ForeignKey("Connection", related_name='connection', on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    created_on = models.IntegerField()
    scheduled_date = models.CharField(max_length=50)

