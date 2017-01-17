from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
# Create your views here.

from . import forms
from . import models
import SystemManage

from datetime import datetime
import os
@csrf_exempt
@login_required
def hostList(request):
    if request.method=='POST':
        form = forms.HostSearchForm(request.POST,user=request.user)
        if form.is_valid():
            data = form.cleaned_data
            if request.user.is_superuser:
                tableData = models.Host.objects.filter(isDel=False)
            else:
                tableData = models.Host.objects.filter(isDel=False).filter(hostgroup__user=request.user)
            if data['name']:
                tableData = tableData.filter(name__icontains=data['name'])
            if data['addr']:
                tableData = tableData.filter(ip__icontains=data['addr'])
            if data['port']:
                tableData = tableData.filter(port=data['port'])
            if data['group']:
                tableData = tableData.filter(hostgroup=data['group'])
            paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
            page = int(request.GET.get('page',1))                 #模板需要
            start = max(page-5,0)
            page_range = paginator.page_range[start:start+10]      #模板需要
            cur_page = paginator.page(page)                        #模板需要
        return render(request,'HostManage/hostlisttable.html',locals())
    else:
        form = forms.HostSearchForm(user=request.user)
    return render(request,'HostManage/hostList.html',locals())


def addHost(request):
    if request.method=='POST':
        form = forms.HostAddForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse(dict(ret=0))
        messages.error(request,form.errors)
    else:
        form = forms.HostAddForm()
    return render(request,'HostManage/addhost.html',locals())

def importHost(request):
    if request.method=='POST':
        file = request.FILES['importhostFile']
        now = datetime.now()
        date = now.strftime('%Y%m%d%H%M%S')
        filename='%s-%s-importhost'%(date,request.user.username)+'.'+file.name.rsplit('.')[-1]
        filename = os.path.join(settings.BASE_DIR,'importFile',filename)
        with open(filename,'wb') as f:
            while True:
                chunk = file.read(1024)
                if not chunk:break
                f.write(chunk)
        return JsonResponse(dict(ret=0))
    else:
        return render(request,'HostManage/importhost.html')

def hostDetail(request,host_id):
    host = models.Host.objects.select_related().get(pk=host_id)
    # host={
    #     'name':'测试主机',
    #     'hostinfo':dict(
    #         OS='CentOS',
    #         cpu_version='Exon 5202 2.5 GHz',
    #         kernal_version='Linux',
    #         mem_total='4G',
    #         disk_total='500G',
    #         MAC='00:00:00:00:00',
    #     )
    # }
    return render(request,'HostManage/hostDetail.html',locals())

def editHost(request,host_id):
    host = models.Host.objects.get(pk=host_id)
    if request.method=='POST':
        data = request.POST
        host.name = data['name']
        host.addr = data['addr']
        host.port = data['port']
        host.username = data['username']
        if data['password']:host.password = data['password']
        host.remark = data['remark']
        try:
            host.save()
            return JsonResponse(dict(ret=0))
        except:
            form = forms.HostAddForm(request.POST)
    else:
        form = forms.HostAddForm(instance=host)
    return render(request,'HostManage/edithost.html',locals())

@csrf_exempt
def deleteHost(request,host_id):
    host = models.Host.objects.get(pk=host_id)
    host.isDel = True
    host.save()
    return JsonResponse(dict(ret=0))
