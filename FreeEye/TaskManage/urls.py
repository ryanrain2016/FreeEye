from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^CommandDispatch/',views.commandTask,name='commandtask'),
    url(r'^FileDispatch/',views.fileTask,name='filetask'),
    url(r'^AddFileTask/',views.addFileTask,name='addfiletask'),
    url(r'^AddCommandTask/',views.addCommandTask,name='addcommandtask'),
    url(r'^FileTaskDetail/(?P<id>\d+)/',views.FileTaskDetail,name='filetaskdetail'),
    url(r'^CommandTaskDetail/(?P<id>\d+)/',views.CommandTaskDetail,name='commandtaskdetail'),
    url(r'^AssignHost/',views.assignHost,name='assignhost'),
    url(r'^GetHostGroup/',views.getHostGroup,name='gethostgroup'),
    url(r'^GetHost/',views.getHost,name='gethost'),
    url(r'^SetHosts/',views.setHosts,name='sethosts'),
]
