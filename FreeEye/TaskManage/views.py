from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings

from . import models
from . import forms
# Create your views here.


@csrf_exempt
@login_required
def fileTask(request):
    if request.method=='POST':
        if request.user.is_superuser:
            tableData = models.FileTask.objects.all()
        else:
            tableData = models.FileTask.objects.filter(hostgroup__user=request.user)
        if data['name']:
            tableData = tableData.filter(name__icontains=data['name'])
        if data['addr']:
            tableData = tableData.filter(ip__icontains=data['addr'])
        if data['port']:
            tableData = tableData.filter(port=data['port'])
        if data['group']:
            tableData = models.Host.objects.filter(hostgroup=data['group'])
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'HostManage/hostlisttable.html',locals())
    else:
        form = forms.FileTaskForm()
    return render(request,'HostManage/hostList.html',locals())
    return render(request,'TaskManage/filetask.html',locals())

def commandTask(request):
    return render(request,'TaskManage/commandtask.html')
