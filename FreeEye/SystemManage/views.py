from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import JsonResponse

from . import models
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
        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'SystemManage/usertablelist.html',locals())
    return render(request,'SystemManage/userList.html',locals())


def addUser(request):
    pass
