from django.core.management.base import BaseCommand,CommandError  
from MainFrame import models
import HostManage
import SystemManage
class Command(BaseCommand):
    help = '初始化所有的数据'

    def initMenu(self):
        HostManage.models.Application.objects.all().delete()
        HostManage.models.Application(appName='apache',
            cmdline='httpd',
            cmdArgs='',
            startCommand='service httpd start',
            stopCommand='service httpd stop',
            restartCommand='service httpd restart').save()
        HostManage.models.Application(appName='nginx',
            cmdline='nginx',
            cmdArgs='',
            startCommand='service nginx start',
            stopCommand='service nginx stop',
            restartCommand='service nginx restart').save()
        HostManage.models.Application(appName='tomcat',
            cmdline='tomcat',
            cmdArgs='',
            startCommand='service tomcat start',
            stopCommand='service tomcat stop',
            restartCommand='service tomcat restart').save()
        HostManage.models.Application(appName='mysql',
            cmdline='mysqld',
            cmdArgs='',
            startCommand='service mysqld start',
            stopCommand='service mysqld stop',
            restartCommand='service mysqld restart').save()
        print('应用程序数据初始化完成！')
        SystemManage.models.Module.objects.all().delete()
        SystemManage.models.Function.objects.all().delete()
        m1 = SystemManage.models.Module(name='主机管理')
        m1.save()
        SystemManage.models.Function(name='查看主机',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='添加主机',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='导入主机',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='主机详情',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='加到首页',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='日志清理设置',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='修改主机',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='删除主机',
            path_reg=r'',
            module=m1).save()
        SystemManage.models.Function(name='WebShell',
            path_reg=r'',
            module=m1).save()
        m2 = SystemManage.models.Module(name='任务管理')
        m2.save()
        SystemManage.models.Function(name='文件分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='添加文件分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='文件任务详情',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='执行文件分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='重新执行文件分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='命令分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='添加命令分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='命令任务详情',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='执行命令分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='重新执行命令分发',
            path_reg=r'',
            module=m2).save()
        SystemManage.models.Function(name='分配主机',
            path_reg=r'',
            module=m2).save()
        m3 = SystemManage.models.Module(name='系统管理')
        m3.save()
        SystemManage.models.Function(name='查看主机组',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='添加主机组',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='编辑主机组',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='删除主机组',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='主机组分配主机',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='主机组分配用户',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='查看用户',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='添加用户',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='删除用户',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='分配用户角色',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='重置用户密码',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='审计日志',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='查看角色',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='添加角色',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='删除角色',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='编辑角色',
            path_reg=r'',
            module=m3).save()
        SystemManage.models.Function(name='分配权限',
            path_reg=r'',
            module=m3).save()
        print('权限数据初始化完成！')
        
    def handle(self,*args,**options):
        self.initMenu()
