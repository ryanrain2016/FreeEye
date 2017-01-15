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
    commandtask = models.ForeignKey(CommandTask)
    taskhost = models.ForeignKey('HostManage.Host')
    is_start = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    finishAt = models.DateTimeField(auto_now=True)

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
    commandtask = models.ForeignKey(CommandTask)
    taskhost = models.ForeignKey('HostManage.Host')
    is_start = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)
    createAt = models.DateTimeField(auto_now_add=True)
    finishAt = models.DateTimeField(default=None,null=True)
