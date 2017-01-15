from django.conf.urls import url
from . import views

urlpatterns=[
    url('^HostList/', views.hostList, name='hostlist'),
    url(r'^AddHost/',views.addHost,name='addhost'),
    url(r'^ImportHost/',views.importHost,name='importhost'),
    url(r'^HostDetail/(?P<host_id>\d+)',views.hostDetail,name='hostdetail'),
    url(r'^EditHost/(?P<host_id>\d+)',views.editHost,name = 'edithost'),
    url(r'^DeleteHost/(?P<host_id>\d+)',views.deleteHost,name='deletehost'),
]
