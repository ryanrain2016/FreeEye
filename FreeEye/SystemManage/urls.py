from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^GroupManage/',views.hostGroupList,{'code':'查看主机组'},name='hostgrouplist'),
    url(r'^AddHostGroup/',views.addHostGroup,{'code':'添加主机组'},name='addhostgroup'),
    url(r'^EditHostGroup/(?P<id>\d+)/',views.editHostGroup,{'code':'编辑主机组'},name='edithostgroup'),
    url(r'^DeleteHostGroup/(?P<id>\d+)/',views.deleteHostgroup,{'code':'删除主机组'},name='deletehostgroup'),
    url(r'^GroupAssignHost/(?P<id>\d+)/',views.groupAssignHost,{'code':'主机组分配主机'},name='groupassignhost'),
    url(r'^GroupAssignUser/(?P<id>\d+)/',views.groupAssignUser,{'code':'主机组分配用户'},name='groupassignuser'),
    url(r'^UserManage/',views.userList,{'code':'查看用户'},name='userlist'),
    url(r'^AddUser/',views.addUser,{'code':'添加用户'},name='adduser'),
    url(r'^DeleteUser/(?P<id>\d+)/',views.deactiveUser,{'code':'删除用户'},name='deleteuser'),
    url(r'^ResetPassword/(?P<id>\d+)/',views.resetPassword,{'code':'重置用户密码'},name='resetpassword'),
    url(r'^UserAssignRole/(?P<id>\d+)/',views.userAssignRole,{'code':'分配用户角色'},name='userassginrole'),
    url(r'^RoleManage/',views.RoleManage,{'code':'查看角色'},name='rolemanage'),
    url(r'^AddRole/',views.addRole,{'code':'添加角色'},name='addrole'),
    url(r'^EditRole/(?P<id>\d+)/',views.editRole,{'code':'编辑角色'},name='editrole'),
    url(r'^DeleteRole/(?P<id>\d+)/',views.deleteRole,{'code':'删除角色'},name='deleterole'),
    url(r'^AssignPerm/(?P<id>\d+)/',views.assignPerm,{'code':'分配权限'},name='assignperm'),
    url(r'^AuditLog/',views.auditLog,{'code':'审计日志'},name='auditlog'),
]
