from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
from .models import Profile
from .forms import ProfileForm
import json,os,re
from datetime import datetime
from SystemManage.models import Function

import HostManage,TaskManage
# Create your views here.
def jsonify(**kw):
    return HttpResponse(json.dumps(dict(**kw)),content_type='json/application')

@login_required
def mainframe(request):
    roles =[ group.name for group in  request.user.groups.all()]
    roles = ','.join(roles)
    perm_hostmanage = Function.objects.get(name='查看主机')
    perm_filetask = Function.objects.get(name='文件分发')
    perm_commandtask = Function.objects.get(name='命令分发')
    perm_usermanage = Function.objects.get(name='查看用户')
    perm_hostgroup = Function.objects.get(name='查看主机组')
    perm_auditlog = Function.objects.get(name='审计日志')
    perm_rolemanage = Function.objects.get(name='查看角色')
    return render(request,'mainframe.html',locals())

def login(request):
    if request.method=='POST' and request.POST:
        u = authenticate(username=request.POST.get('username',None),
            password=request.POST.get('password',None))
        if u is not None:
            if u.is_active:
                _login(request, u)
                next = request.GET.get('next',settings.LOGIN_DIRECT)
                return redirect(next)
            else:
                messages.error(request, '用户未激活！')
        else:
            messages.error(request, '用户名或者密码错误！')
    return render(request,'login.html',locals())

def logout(request):
    _logout(request)
    return redirect('/')

@login_required
@csrf_exempt
def avatar_form(request):
    if request.method=='GET':
        return render(request,'MainFrame/form_avatar.html')
    avatar = request.FILES.get('avatar',None)
    if avatar is None:return jsonify(ret=-1)
    username = request.user.username
    filename = os.path.join(settings.MEDIA_ROOT,'avatar',username+'.png')
    with open(filename, 'wb+') as destination:
        for chunk in avatar.chunks():
            destination.write(chunk)
    url = settings.MEDIA_URL + 'avatar/'+username+'.png'
    user = request.user
    if hasattr(user,'profile'):
        p = user.profile
        p.avatar=url
        p.save()
    else:
        p = Profile(avatar=url)
        p.user = user
        p.save()
    return jsonify(ret=0,avatar=p.avatar)

@login_required
def profile_form(request):
    u = request.user
    if hasattr(u,'profile'):
        p = u.profile
    else:
        p = Profile()
    if request.method == 'GET':
        form = ProfileForm(instance=p)
        return render(request,'MainFrame/form_profile.html',locals())
    else:
        p.user = u
        form = ProfileForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
        return render(request,'MainFrame/form_profile.html',locals())

@login_required
def index(request):
    now = datetime.now()
    if request.user.is_superuser:
        hosts = HostManage.models.Host.objects.filter(isDel=False)
    else:
        hosts = HostManage.models.Host.objects.filter(isDel=False).filter(hostgroup__user=request.user)
    host_total = hosts.count()
    host_online = hosts.filter(active=True).count()
    hosts = request.user.host_set.all()
    if request.user.is_superuser:
        filetask_total = TaskManage.models.FileTaskProgress.objects
        commandtask_total = TaskManage.models.CommandTaskProgress.objects
        filetask_finished= TaskManage.models.FileTaskProgress.objects.filter(is_finish=True)
        commandtask_finished = TaskManage.models.CommandTaskProgress.objects.filter(is_finish=True)
    else:
        filetask_total = TaskManage.models.FileTaskProgress.objects.filter(createBy=request.user)
        commandtask_total = TaskManage.models.CommandTaskProgress.objects.filter(createBy=request.user)
        filetask_finished= TaskManage.models.FileTaskProgress.objects.filter(task__createBy=request.user).filter(is_finish=True)
        commandtask_finished = TaskManage.models.CommandTaskProgress.objects.filter(task__createBy=request.user).filter(is_finish=True)
    task_total = filetask_total.count()+commandtask_total.count()
    task_finished = filetask_finished.count() + commandtask_finished.count()

    filetask_last3 = TaskManage.models.FileTask.objects.order_by('-createAt').all()[:3]
    filetasks = []
    for filetask in filetask_last3:
        total = filetask_total.filter(task=filetask).count()
        finished = filetask_total.filter(task=filetask).filter(is_finish=True).count()
        filetasks.append(dict(name=filetask.name,total=total,finished=finished,createAt=filetask.createAt))
    commandtask_last3 = TaskManage.models.CommandTask.objects.order_by('-createAt').all()[:3]
    commandtasks = []
    for commandtask in commandtask_last3:
        total = commandtask_total.filter(task=command).count()
        finished = commandtask_total.filter(task=command).filter(is_finish=True).count()
        commandtasks.append(dict(name=commandtask.name,total=total,finished=finished,createAt=filetask.createAt))
    return render(request,'home.html',locals())

