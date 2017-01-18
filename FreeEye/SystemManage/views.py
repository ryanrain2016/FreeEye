from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q

import HostManage

from . import models
from . import forms
# Create your views here.
@csrf_exempt
@login_required
def hostGroupList(request):
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

def addHostGroup(request):
    if request.method=='POST':
        group = models.HostGroup(name = request.POST['name'])
        try:
            group.save()
            return JsonResponse(dict(ret=0))
        except:
            messages.error(request, '主机组名错误！')
            return render(request,'SystemManage/addhostgroup.html',locals())
    else:
        return render(request,'SystemManage/addhostgroup.html',locals())

def editHostGroup(request,id):
    group = models.HostGroup.objects.get(pk=id)
    if request.method=='POST':
        try:
            group.name = request.POST['name']
            group.save()
            return JsonResponse(dict(ret=0))
        except:
            messages.error(request, '主机组名错误！')
            return render(request,'SystemManage/edithostgroup.html',locals())
    else:
        return render(request,'SystemManage/edithostgroup.html',locals())

@login_required
@csrf_exempt
def deleteHostgroup(request,id):
    group = models.HostGroup.objects.get(pk=id)
    group.delete()
    return JsonResponse(dict(ret=0))

@csrf_exempt
def groupAssignHost(request,id):
    group = models.HostGroup.objects.get(pk=id)
    if request.method=='POST':
        hostIds = request.POST.get('hostIds','')
        group.host_set=[]
        if hostIds=='':
            return JsonResponse(dict(ret=0))
        hostIds = list(map(int,hostIds.split('&')))
        HostManage.models.Host.objects.filter(id__in=hostIds).update(hostgroup=group)
        return JsonResponse(dict(ret=0))
    else:
        hosts = HostManage.models.Host.objects.filter(Q(hostgroup=None)|Q(hostgroup=group))
    return render(request,'SystemManage/assignhost.html',locals())


def userList(request):
    if request.method=='POST':
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        if username:
            tableData = models.User.objects.select_related('profile').filter(username__icontains=username)
        else:
            tableData = models.User.objects.select_related('profile')
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


def addUser(request):
    if request.method=='POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(username=data['username'],password=data['password'])
                user.save()
                return JsonResponse(dict(ret=0))
            except Exception as e:
                return JsonResponse(dict(ret=-1,msg='用户创建失败！'))
        return render(request,'SystemManage/adduser.html',locals())
    else:
        form = forms.UserForm()
        return render(request,'SystemManage/adduser.html',locals())

@login_required
@csrf_exempt
def deactiveUser(request,id):
    user = User.objects.get(pk=id)
    user.is_active=False
    user.save()
    return JsonResponse(dict(ret=0))
