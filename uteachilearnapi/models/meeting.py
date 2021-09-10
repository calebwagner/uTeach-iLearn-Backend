from django.db import models

class Meeting(models.Model):
    connection = models.ForeignKey("Connection", on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    created_on = models.TimeField()
    scheduled_date = models.TimeField()
