from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^HostList/', views.hostList, {'code':'查看主机'},name='hostlist'),
    url(r'^AddHost/',views.addHost, {'code':'添加主机'},name='addhost'),
    url(r'^ImportHost/',views.importHost, {'code':'导入主机'},name='importhost'),
    url(r'^HostDetail/(?P<host_id>\d+)/',views.hostDetail, {'code':'主机详情'},name='hostdetail'),
    url(r'^EditHost/(?P<host_id>\d+)/',views.editHost, {'code':'修改主机'},name = 'edithost'),
    url(r'^DeleteHost/(?P<host_id>\d+)/',views.deleteHost, {'code':'删除主机'},name='deletehost'),
    url(r'^WebShell/(?P<id>\d+)/',views.webshell, {'code':'WebShell'},name='webshell'),
    url(r'^HostStat/(?P<id>\d+)/',views.HostStat, {'code':'主机详情'},name='hoststat'),
    url(r'^(?P<id>\d+)/LogCleanConfig/',views.HostLogCleanConfig, {'code':'日志清理设置'},name='logcleanconfig'),
    url(r'^(?P<id>\d+)/LogCleanConfigDetail/(?P<cfg_id>\d+)/',views.configDetail, {'code':'日志清理设置'},name='configdetail'),
    url(r'^(?P<id>\d+)/AddConfig/',views.addconfig, {'code':'日志清理设置'},name='addconfig'),
    url(r'^DeleteConfig/',views.DeleteConfig, {'code':'日志清理设置'},name='deleteconfig'),
    url(r'^AddToTop/',views.addToTop,{'code':'加到首页'},name='addtotop'),
    url(r'^RemoveFromTop/',views.removeFromTop,name='removefromtop'),
]
