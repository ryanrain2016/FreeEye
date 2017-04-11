from django.db import models
from django.contrib.auth.models import User,Group

# Create your models here.
class HostGroup(models.Model):
    name = models.CharField(max_length=32)
    user = models.ManyToManyField(User,blank=True)
    isDel = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Log(models.Model):
    username = models.CharField(max_length=32,blank=True,null=True)
    do = models.CharField(max_length=128)
    level = models.CharField(max_length=8,default='info',choices={
            ('debug','debug'),('info','info'),('warn','warn'),('error','error'),('fatal','fatal')
        })
    createAt = models.DateTimeField(auto_now_add=True)

class Module(models.Model):
    name = models.CharField(max_length=32)
    app = models.CharField(max_length=32)

    class Meta:
        permissions = (
            ('access_to_module','进入模块'),
        )

class Function(models.Model):
    name = models.CharField(max_length=32)
    path_reg = models.CharField(max_length=128)
    module = models.ForeignKey(Module)

    class Meta:
        permissions = (
            ('access_to_Function','进入功能'),
        )