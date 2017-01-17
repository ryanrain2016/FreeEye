from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HostGroup(models.Model):
    name = models.CharField(max_length=32)
    user = models.ManyToManyField(User,blank=True,null=True)
    isDel = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Log(models.Model):
    user = models.CharField(max_length=32)
    do = models.CharField(max_length=128)
    isnormal = models.BooleanField(default=True)
    createAt = models.DateTimeField(auto_now_add=True)
