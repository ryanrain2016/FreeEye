from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User
import os
from datetime import datetime
from . import models
from . import forms
# Create your views here.
from functools import reduce
import SystemManage
import HostManage
@csrf_exempt
@login_required
def fileTask(request):
    if request.method=='POST':
        data = request.POST
        if request.user.is_superuser:
            tableData = models.FileTask.objects.all()
        else:
            tableData = models.FileTask.objects.filter(createBy=request.user)
        if data['name']:
            tableData = tableData.filter(name__icontains=data['name'])
        if data['file']:
            tableData = tableData.filter(file__icontains=data['file'])
        if data['remote_file']:
            tableData = tableData.filter(remote_file__icontains=data['remote_file'])
        if data['on_exists']:
            tableData = tableData.filter(on_exists=data['on_exists'])
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'TaskManage/filetasktablelist.html',locals())
    else:
        form = forms.FileTaskSearchForm()
    return render(request,'TaskManage/filetask.html',locals())

@login_required
def addFileTask(request):
    if request.method=='POST':
        form = forms.FileTaskForm(request.POST)
        if form.is_valid():
            file = request.FILES.get('file',None)
            if file is None:
                return render(request,'TaskManage/addfiletask.html',locals())
            now = datetime.now()
            date = now.strftime('%Y%m%d%H%M%S')
            os.mkdir(os.path.join(settings.BASE_DIR,'taskfile',date))
            _dir = os.path.join(date,file.name)
            with open(os.path.join(settings.BASE_DIR,'taskfile',_dir),'wb') as f:
                while True:
                    chunk = file.read(1024)
                    if not chunk:break
                    f.write(chunk)
            data = form.cleaned_data
            task = models.FileTask(
                name=data['name'],
                file=_dir,
                remote_file = data['remote_file'],
                on_exists = data['on_exists'],
                createBy = request.user,
            )
            task.save()
            return JsonResponse(dict(ret=0))

    else:
        form = forms.FileTaskForm()
    return render(request,'TaskManage/addfiletask.html',locals())

@csrf_exempt
@login_required
def commandTask(request):
    if request.method=='POST':
        data = request.POST
        if request.user.is_superuser:
            tableData = models.CommandTask.objects.all()
        else:
            tableData = models.CommandTask.objects.filter(createBy=request.user)
        if data['name']:
            tableData = tableData.filter(name__icontains=data['name'])
        if data['cmdline']:
            tableData = tableData.filter(cmdline__icontains=data['cmdline'])
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'TaskManage/commandtasktablelist.html',locals())
    else:
        form = forms.CommandTaskSearchForm()
    return render(request,'TaskManage/commandtask.html',locals())


@login_required
def addCommandTask(request):
    if request.method=='POST':
        form = forms.CommandTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            task = models.CommandTask(
                name=data['name'],
                cmdline=data['cmdline'],
                createBy=request.user,
            )
            task.save()
            return JsonResponse(dict(ret=0))
    else:
        form = forms.CommandTaskForm()
    return render(request,'TaskManage/addcommandtask.html',locals())

@login_required
@csrf_exempt
def FileTaskDetail(request, id):
    taskType = 'file'
    task = models.FileTask.objects.get(pk=id)
    if request.method=='POST':
        page = request.GET.get('page',1)
        tableData = models.FileTaskProgress.objects.filter(task=task)
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'TaskManage/filetaskdetailtablelist.html',locals())
    return render(request,'TaskManage/filetaskdetail.html',locals())

@login_required
def CommandTaskDetail(request, id):
    taskType = 'cmd'
    task = models.CommandTask.objects.get(pk=id)
    return render(request,'TaskManage/commandtaskdetail.html',locals())

def assignHost(request):
    taskType = request.GET.get('taskType','')
    id = request.GET.get('id','')
    if request.method=='POST':
        return render(request,'TaskManage/assignhost.html',locals())
    else:
        return render(request,'TaskManage/assignhost.html',locals())

@csrf_exempt
def getHostGroup(request):
    #hostgroups = User.objects.select_related().get(pk=request.user.id).hostgroup_set
    if request.user.is_superuser:
        hostgroups = SystemManage.models.HostGroup.objects.all()
    else:
        hostgroups = request.user.hostgroup_set.all()
    nodes = [dict(text=group.name,groupid=group.id) for group in hostgroups]
    return JsonResponse([dict(text='全部',
        nodes = nodes,
        groupid=-1
    )],safe=False)

@csrf_exempt
def getHost(request):
    taskType = request.GET.get('taskType','')
    id = request.GET.get('id','')
    hostgroupid = request.POST['groupid']
    if hostgroupid != '-1':
        hosts = SystemManage.models.HostGroup.objects.select_related().get(pk=hostgroupid).host_set.all()
    elif request.user.is_superuser:
        hosts = HostManage.models.Host.objects.all()
    else:
        groups = request.user.hostgroup_set.all()
        hosts = [group.host_set for group in groups]
        hosts = reduce(lambda x,y:x|y,hosts) if hosts else []
    taskmodel = models.FileTask if taskType == 'file' else models.CommandTask
    task = taskmodel.objects.get(pk=id)
    taskprogressmodel = models.FileTaskProgress if taskType=='file' else models.CommandTaskProgress
    taskprogress = taskprogressmodel.objects.filter(task = task).select_related().all()
    selected_hosts = [p.taskhost for p in taskprogress]
    hosts = [dict(id=host.id,name=host.name,checked=host in selected_hosts) for host in hosts.all()]
    return JsonResponse(hosts,safe=False)

@csrf_exempt
def setHosts(request):
    taskType = request.POST.get('taskType','')
    id = request.POST.get('id','')
    hostIds = request.POST.get('hostIds','')
    if not hostIds:return JsonResponse(dict(ret=0))
    hostIds = hostIds.split('&')
    taskmodel = models.FileTask if taskType == 'file' else models.CommandTask
    task = taskmodel.objects.get(pk=id)
    taskprogressmodel = models.FileTaskProgress if taskType=='file' else models.CommandTaskProgress
    taskprogress = taskprogressmodel.objects.filter(task = task).select_related().all()
    selected_hosts = [str(p.taskhost.id) for p in taskprogress]
    for hostid in hostIds:
        if not hostid:
            break
        if hostid in selected_hosts:
            continue
        p = taskprogressmodel(task=task,taskhost=HostManage.models.Host.objects.get(pk=hostid))
        p.save()
    return JsonResponse(dict(ret=0))
