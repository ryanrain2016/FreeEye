from django.db import models

# Create your models here.

class Alert(models.Model):
    name = models.CharField(max_length=32)
    _type = models.CharField(max_length=8)
