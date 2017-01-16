from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings
from django.conf import settings
import os
from datetime import datetime
from . import models
from . import forms
# Create your views here.


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
def FileTaskDetail(request, id):
    return render(request,'TaskManage/filetaskdetail.html',locals())

@login_required
def CommandTaskDetail(request, id):
    return render(request,'TaskManage/commandtaskdetail.html',locals())
