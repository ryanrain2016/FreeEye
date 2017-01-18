from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^GroupManage/',views.hostGroupList,name='hostgrouplist'),
    url(r'^AddHostGroup/',views.addHostGroup,name='addhostgroup'),
    url(r'^EditHostGroup/(?P<id>\d+)/',views.editHostGroup,name='edithostgroup'),
    url(r'^DeleteHostGroup/(?P<id>\d+)/',views.deleteHostgroup,name='deletehostgroup'),
    url(r'^GroupAssignHost/(?P<id>\d+)/',views.groupAssignHost,name='groupassignhost'),
    url(r'^UserManage/',views.userList,name='userlist'),
    url(r'^AddUser/',views.addUser,name='adduser'),
    url(r'^DeleteUser/(?P<id>\d+)/',views.deactiveUser,name='deleteuser'),
]
