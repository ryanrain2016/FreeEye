from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class HostGroup(models):
    name = models.CharField(max_length=32)
    user = models.ManyToManyField(User,blank=True,null=True)

    def __self__(self):
        return self.name
