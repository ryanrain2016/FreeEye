from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Alert(models.Model):
    name = models.CharField(max_length=32)
    _type = models.CharField(max_length=4,choices=(('email','邮件'),('sms','短信')))
    factor = models.CharField(max_length=4,choices=(('dis','磁盘'),('cpu','CPU'),('mem','内存'),('net','带宽'),('app','应用')))
    threshold = models.IntegerField(default=0,blank=True)
    receiver = models.CharField(default='auto',max_length=128)
    active = models.BooleanField(default=True)
    alertContent = models.CharField(default=None,null=True,blank=True,max_length=1024)
    createBy = models.ForeignKey(User)

class AlertRecord(models.Model):
    alert = models.ForeignKey(Alert)
    host = models.ForeignKey('HostManage.Host')
