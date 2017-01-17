from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CommandTask(models.Model):
    name = models.CharField(max_length=32)
    cmdline = models.CharField(max_length=256)
    createBy = models.ForeignKey(User)
    start = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

class CommandTaskProgress(models.Model):
    task = models.ForeignKey(CommandTask)
    taskhost = models.ForeignKey('HostManage.Host')
    output = models.CharField(max_length=4096,default='')
    is_start = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)
    result =models.CharField(max_length=8,null=True,blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    finishAt = models.DateTimeField(null=True,default=None)

class FileTask(models.Model):
    name = models.CharField(max_length=32)
    file = models.CharField(max_length=256)
    remote_file = models.CharField(max_length=256)
    on_exists = models.CharField(max_length=4,choices=(('ov','覆盖'),('ba','备份'),('sk','跳过')))
    createBy = models.ForeignKey(User)
    start = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)

class FileTaskProgress(models.Model):
    task = models.ForeignKey(FileTask)
    taskhost = models.ForeignKey('HostManage.Host')
    is_start = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)
    result =models.CharField(max_length=8,null=True,blank=True)
    createAt = models.DateTimeField(auto_now_add=True)
    finishAt = models.DateTimeField(null=True,default=None)
