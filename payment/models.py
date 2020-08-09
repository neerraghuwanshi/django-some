from django.db import models
from datetime import timezone
from django.contrib.auth.models import User


class Betting(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.TextField()
    amount = models.IntegerField(default = 0)  
    option = models.CharField(max_length=100) 
    checksum = models.CharField(max_length=100, null=True, blank=True) 
    user = models.ForeignKey(User,related_name='leads', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.title