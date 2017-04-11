from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Menu(models.Model):
#     title = models.CharField(max_length=32)
#     url = models.CharField(max_length=32,null=True,blank=True,default='')
#     icon = models.CharField(max_length=32,null=True,blank=True,default='')
#     parent = models.ForeignKey('self',related_name='submenu',blank=True,null=True)

#     def __str__(self):
#         return self.title + ' | ' + (self.url if self.url else '') + '|' + (self.icon if self.icon else '')

#     class Meta:
#         verbose_name = '菜单'
#         verbose_name_plural = '菜单'
#         permissions = (("can_view_menu","查看菜单"),)
#         default_permissions = ()

class Profile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.CharField(max_length=64,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(max_length=100,null=True,blank=True)
