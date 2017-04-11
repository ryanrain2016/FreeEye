from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^CommandDispatch/',views.commandTask, {'code':'命令分发'},name='commandtask'),
    url(r'^FileDispatch/',views.fileTask, {'code':'文件分发'},name='filetask'),
    url(r'^AddFileTask/',views.addFileTask, {'code':'添加文件分发'},name='addfiletask'),
    url(r'^AddCommandTask/',views.addCommandTask, {'code':'添加命令分发'},name='addcommandtask'),
    url(r'^FileTaskDetail/(?P<id>\d+)/',views.FileTaskDetail, {'code':'文件任务详情'},name='filetaskdetail'),
    url(r'^CommandTaskDetail/(?P<id>\d+)/',views.CommandTaskDetail, {'code':'命令任务详情'},name='commandtaskdetail'),
    url(r'^AssignHost/',views.assignHost, {'code':'分配主机'},name='assignhost'),
    url(r'^GetHostGroup/',views.getHostGroup, {'code':'分配主机'},name='gethostgroup'),
    url(r'^GetHost/',views.getHost, {'code':'分配主机'},name='gethost'),
    url(r'^SetHosts/',views.setHosts, {'code':'分配主机'},name='sethosts'),
]
