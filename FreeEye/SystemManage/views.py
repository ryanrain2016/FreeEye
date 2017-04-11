from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse,HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q

from guardian.shortcuts import assign_perm,remove_perm

import HostManage
from guardian.decorators import permission_required
from guardian.core import ObjectPermissionChecker
from . import models
from . import forms
from .models import Function
from FreeEye import utils
logger = utils.Logger()
# Create your views here.
@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def hostGroupList(request,code):
    checker = ObjectPermissionChecker(request.user)
    add = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='添加主机组'))
    edit = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='编辑主机组'))
    delete = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='删除主机组'))
    assignhost = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='主机组分配主机'))
    assignuser = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='主机组分配用户'))
    if request.method=='POST':
        name = request.POST.get('name','')
        if name:
            tableData = models.HostGroup.objects.filter(name__icontains=name).all()
        else:
            tableData = models.HostGroup.objects.all()
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'SystemManage/hostgrouptablelist.html',locals())
    return render(request,'SystemManage/hostGroupList.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def addHostGroup(request,code):
    if request.method=='POST':
        group = models.HostGroup(name = request.POST['name'])
        try:
            group.save()
            logger.log(request,'添加了主机组(%s)'%group.name)
            return JsonResponse(dict(ret=0))
        except:
            logger.error(request,'添加了主机组(%s)，错误'%group.name)
            messages.error(request, '主机组名错误！')
            return render(request,'SystemManage/addhostgroup.html',locals())
    else:
        return render(request,'SystemManage/addhostgroup.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def editHostGroup(request,id,code):
    group = models.HostGroup.objects.get(pk=id)
    if request.method=='POST':
        try:
            group.name = request.POST['name']
            group.save()
            logger.log(request,'编辑了主机组(%s)'%group.name)
            return JsonResponse(dict(ret=0))
        except:
            logger.error(request,'编辑了主机组(%s)，错误'%group.name)
            messages.error(request, '主机组名错误！')
            return render(request,'SystemManage/edithostgroup.html',locals())
    else:
        return render(request,'SystemManage/edithostgroup.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def deleteHostgroup(request,id,code):
    group = models.HostGroup.objects.get(pk=id)
    group.delete()
    logger.warn(request,'删除了主机组(%s)'%group.name)
    return JsonResponse(dict(ret=0))

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def groupAssignHost(request,id,code):
    group = models.HostGroup.objects.get(pk=id)
    if request.method=='POST':
        hostIds = request.POST.get('hostIds','')
        group.host_set=[]
        if hostIds=='':
            return JsonResponse(dict(ret=0))
        hostIds = list(map(int,hostIds.split('&')))
        hosts = HostManage.models.Host.objects.filter(id__in=hostIds).all()
        hosts.update(hostgroup=group)
        hostname = ','.join([host.name for host in hosts])
        logger.log(request,'将主机组(%s)分配了主机(%s)'%(group.name,hostname))
        return JsonResponse(dict(ret=0))
    else:
        hosts = HostManage.models.Host.objects.filter(Q(hostgroup=None)|Q(hostgroup=group))
    return render(request,'SystemManage/assignhost.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def groupAssignUser(request,id,code):
    group = models.HostGroup.objects.select_related().get(pk=id)
    if request.method=='POST':
        userIds = request.POST.get('userIds','')
        group.user=[]
        if userIds=='':
            return JsonResponse(dict(ret=0))
        userIds = list(map(int,userIds.split('&')))
        users = User.objects.filter(id__in=userIds)
        group.user=users
        username = ','.join([user.username for user in users])
        logger.log(request,'将主机组(%s)分配给了用户(%s)'%(group.name,username))
        return JsonResponse(dict(ret=0))
    else:
        users = User.objects.filter(is_superuser=False).filter(is_active=True).exclude(username='AnonymousUser').all()
        # users = [dict(id=user.id,user.username,checked = (user in group.user)) for user in users]
    return render(request,'SystemManage/assignuser.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def userList(request,code):
    checker = ObjectPermissionChecker(request.user)
    add = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='添加用户'))
    delete = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='删除用户'))
    assignrole = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='分配用户角色'))
    resetpassword = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='重置用户密码'))
    if request.method=='POST':
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        tableData = models.User.objects.select_related('profile')
        if username:
            tableData=tableData.exclude(username='AnonymousUser').filter(username__icontains=username)
        else:
            tableData = tableData.exclude(username='AnonymousUser')
        if email:
            tableData = tableData.filter(profile__email__icontains=email)
        tableData = tableData.filter(is_active=True).filter(is_superuser=False)
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'SystemManage/usertablelist.html',locals())
    return render(request,'SystemManage/userList.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def addUser(request,code):
    if request.method=='POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(username=data['username'],password=data['password'])
                user.save()
                logger.log(request,'添加了用户(%s)'%(user.username))
                return JsonResponse(dict(ret=0))
            except Exception as e:
                logger.error(request,'添加用户(%s)错误，'%(data['username']))
                return JsonResponse(dict(ret=-1,msg='用户创建失败！'))
        return render(request,'SystemManage/adduser.html',locals())
    else:
        form = forms.UserForm()
        return render(request,'SystemManage/adduser.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def deactiveUser(request,id,code):
    user = User.objects.get(pk=id)
    user.is_active=False
    user.save()
    logger.warn(request,'删除了用户(%s)!'%(user.username))
    return JsonResponse(dict(ret=0))

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def userAssignRole(request,id,code):
    user = User.objects.get(pk=id)
    roles = models.Group.objects.all()
    if request.method=='POST':
        roleIds = request.POST.get('roleIds','')
        user.groups=[]
        if roleIds=='':
            return JsonResponse(dict(ret=0))
        roleIds = list(map(int,roleIds.split('&')))
        roles = models.Group.objects.filter(id__in=roleIds)
        user.groups=roles
        rolename = ','.join([role.name for role in roles])
        logger.log(request,'给用户(%s)分配了角色(%s)!'%(user.username,rolename))
        return JsonResponse(dict(ret=0))
    else:
        return render(request,'SystemManage/assignrole.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def resetPassword(request,id,code):
    user = User.objects.get(pk=id)
    if request.method=='POST':
        p1 = request.POST.get('pass1','')
        p2 = request.POST.get('pass2','')
        if p1 and p1==p2:
            user.set_password(p1)
            user.save()
            logger.warn(request,'重置了用户(%s)密码！'%(user.username))
            return JsonResponse(dict(ret=0))
        errors='密码输入错误'
    return render(request,'SystemManage/resetpassword.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def RoleManage(request,code):
    checker = ObjectPermissionChecker(request.user)
    add = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='添加角色'))
    delete = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='删除角色'))
    edit = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='编辑角色'))
    assignperm = checker.has_perm('SystemManage.access_to_Function',Function.objects.get(name='分配权限'))

    if request.method=='POST':
        name = request.POST.get('name','')
        if name:
            tableData = models.Group.objects.filter(name__icontains=name).all()
        else:
            tableData = models.Group.objects.all()
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'SystemManage/roletablelist.html',locals())
    else:
        return render(request,'SystemManage/roleList.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def addRole(request,code):
    if request.method=='POST':
        group = models.Group(name = request.POST['name'])
        try:
            group.save()
            logger.log(request,'添加了角色(%s)！'%(group.name))
            return JsonResponse(dict(ret=0))
        except:
            logger.error(request,'添加了角色(%s)错误！'%(request.POST['name']))
            messages.error(request, '角色名错误！')
            return render(request,'SystemManage/addrole.html',locals())
    else:
        return render(request,'SystemManage/addrole.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def editRole(request,id,code):
    group = models.Group.objects.get(pk=id)
    if request.method=='POST':
        try:
            group.name = request.POST['name']
            group.save()
            logger.log(request,'编辑了角色(%s)！'%(group.name))
            return JsonResponse(dict(ret=0))
        except:
            messages.error(request, '角色名错误！')
            return render(request,'SystemManage/editrole.html',locals())
    else:
        return render(request,'SystemManage/editrole.html',locals())

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
@csrf_exempt
def deleteRole(request,id,code):
    group = models.Group.objects.get(pk=id)
    group.delete()
    logger.error(request,'删除了角色(%s)！'%(group.name))
    return JsonResponse(dict(ret=0))

@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def assignPerm(request,id,code):
    role = models.Group.objects.get(pk=id)
    if request.method=='POST':
        remove_perm('access_to_Function',role,models.Function.objects.all())
        for k in request.POST:
            if k.startswith('function'):
                function_id = int(k.split('_')[1])
                func = models.Function.objects.get(pk=function_id)
                assign_perm('access_to_Function',role,func)
        logger.error(request,'分配了角色(%s)权限！'%(role.name))
        return JsonResponse(dict(ret=0))
    else:
        modules = models.Module.objects.select_related().all()
    return render(request,'SystemManage/assignPerm.html',locals())


@permission_required('SystemManage.access_to_Function',(models.Function,'name','code'))
def auditLog(request,code):
    if request.method=='POST':
        username = request.POST.get('username','')
        level = request.POST.get('level','')
        tableData = models.Log.objects.order_by('-createAt')
        if username:
            tableData = tableData.filter(username=username)
        if level:
            tableData = tableData.filter(level=level)
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'SystemManage/auditlogtable.html',locals())
    return render(request,'SystemManage/auditlog.html',locals())