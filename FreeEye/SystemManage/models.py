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
