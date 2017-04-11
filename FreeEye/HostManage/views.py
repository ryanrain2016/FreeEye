from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site
# Create your views here.

from channels import Channel

from . import forms
from . import models
import SystemManage

from datetime import datetime
import os,time
from guardian.decorators import permission_required
from SystemManage.models import Function
from FreeEye import utils
logger = utils.Logger()

@csrf_exempt
@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def hostList(request,code):
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
            perm_detail = Function.objects.get(name='主机详情')
            perm_tohome = Function.objects.get(name='加到首页')
            perm_config = Function.objects.get(name='日志清理设置')
            perm_edit = Function.objects.get(name='修改主机')
            perm_delete = Function.objects.get(name='删除主机')
            perm_webshell = Function.objects.get(name='WebShell')
        return render(request,'HostManage/hostlisttable.html',locals())
    else:
        form = forms.HostSearchForm(user=request.user)
        perm_add = Function.objects.get(name='添加主机')
        perm_import = Function.objects.get(name='导入主机')
    return render(request,'HostManage/hostList.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def addHost(request,code):
    if request.method=='POST':
        form = forms.HostAddForm(request.POST)
        if form.is_valid():
            host = form.save()
            logger.log(request,'添加了主机%s(%s).'%(host.name,host.addr))
            site = get_current_site(request)
            ws_protocol = 'wss' if request.is_secure() else 'ws'
            Channel('HostAdd').send(dict(id = host.id,site=site,ws_protocol=ws_protocol))
            return JsonResponse(dict(ret=0))
        messages.error(request,form.errors)
    else:
        form = forms.HostAddForm()
    return render(request,'HostManage/addhost.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def importHost(request,code):
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
        site = get_current_site(request)
        ws_protocol = 'wss' if request.is_secure() else 'ws'
        Channel('HostImport').send(dict(site=site,ws_protocol=ws_protocol,file=filename))
        return JsonResponse(dict(ret=0))
    else:
        return render(request,'HostManage/importhost.html')

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def hostDetail(request,host_id,code):
    host = models.Host.objects.select_related().get(pk=host_id)
    return render(request,'HostManage/hostDetail.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def editHost(request,host_id,code):
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
            logger.log(request,'编辑了主机%s(%s).'%(host.name,host.addr))
            site = get_current_site(request)
            ws_protocol = 'wss' if request.is_secure() else 'ws'
            Channel('HostAdd').send(dict(id = host.id,site=site,ws_protocol=ws_protocol))
            return JsonResponse(dict(ret=0))
        except:
            form = forms.HostAddForm(request.POST)
    else:
        form = forms.HostAddForm(instance=host)
    return render(request,'HostManage/edithost.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
@csrf_exempt
def deleteHost(request,host_id,code):
    host = models.Host.objects.get(pk=host_id)
    host.isDel = True
    host.save()
    logger.log(request,'删除了主机%s(%s).'%(host.name,host.addr))
    return JsonResponse(dict(ret=0))

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def webshell(request,id,code):
    host = models.Host.objects.get(pk=id)
    logger.log(request,'连接了主机%s(%s)的shell.'%(host.name,host.addr))
    if not request.user.is_superuser and request.user not in host.hostgroup.user:
        return HttpResponse('403 Not Allowed')
    return render(request,'HostManage/webshell.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def HostStat(request,id,code):
    stats = models.HostStat.objects.filter(host_id=id).order_by('-createAt')[:20]
    stats = list(stats)[::-1]
    cpu_usr=[]
    cpu_sys=[]
    cpu_idle=[]
    mem_total=[]
    mem_used=[]
    mem_free=[]
    mem_avai=[]
    net_sent=[]
    net_recv=[]
    disk_write=[]
    disk_read=[]
    createAt=[]
    for stat in stats:
        cpu_usr.append(stat.cpu_usr)
        cpu_sys.append(stat.cpu_sys)
        cpu_idle.append(stat.cpu_idle)
        mem_total.append(stat.mem_total)
        mem_used.append(stat.mem_used)
        mem_free.append(stat.mem_free)
        mem_avai.append(stat.mem_avai)
        net_recv.append(stat.net_recv)
        net_sent.append(stat.net_sent)
        disk_write.append(stat.disk_write)
        disk_read.append(stat.disk_read)
        createAt.append(stat.createAt)
    labels = list(map(time2str,createAt))
    cpudatasets=[]
    cpudatasets.append(dict(
        backgroundColor="rgba(220,220,220,0.5)",
        borderColor = "rgba(220,220,220,1)",
        pointBackgroundColor = "rgba(220,220,220,1)",
        pointBorderColor = "#fff",
        data = cpu_usr,
        label = 'usr'
        ))
    cpudatasets.append(dict(
        backgroundColor="rgba(151,187,205,0.5)",
        borderColor = "rgba(151,187,205,1)",
        pointBackgroundColor = "rgba(151,187,205,1)",
        pointBorderColor = "#fff",
        data = cpu_sys,
        label = 'sys'
        ))
    cpudatasets.append(dict(
        backgroundColor="rgba(78,151,205,0.5)",
        borderColor = "rgba(78,151,205,1)",
        pointBackgroundColor = "rgba(78,151,205,1)",
        pointBorderColor = "#fff",
        data = cpu_idle,
        label = 'idle'
        ))
    cpudata=dict(labels=labels,datasets=cpudatasets)
    memdatasets=[]
    memdatasets.append(dict(
        backgroundColor="rgba(220,220,220,0.5)",
        borderColor = "rgba(220,220,220,1)",
        pointBackgroundColor = "rgba(220,220,220,1)",
        pointBorderColor = "#fff",
        data = mem_total,
        label = 'Total'
        ))
    memdatasets.append(dict(
        backgroundColor="rgba(151,187,205,0.5)",
        borderColor = "rgba(151,187,205,1)",
        pointBackgroundColor = "rgba(151,187,205,1)",
        pointBorderColor = "#fff",
        data = mem_used,
        label = 'used'
        ))
    memdatasets.append(dict(
        backgroundColor="rgba(78,151,205,0.5)",
        borderColor = "rgba(78,151,205,1)",
        pointBackgroundColor = "rgba(78,151,205,1)",
        pointBorderColor = "#fff",
        data = mem_free,
        label = 'free'
        ))
    memdatasets.append(dict(
        backgroundColor="rgba(23,151,205,0.5)",
        borderColor = "rgba(156,151,205,1)",
        pointBackgroundColor = "rgba(46,151,205,1)",
        pointBorderColor = "#fff",
        data = mem_avai,
        label = 'available'
        ))
    memdata=dict(labels=labels,datasets=memdatasets)
    netdatasets=[]
    netdatasets.append(dict(
        backgroundColor="rgba(220,220,220,0.5)",
        borderColor = "rgba(220,220,220,1)",
        pointBackgroundColor = "rgba(220,220,220,1)",
        pointBorderColor = "#fff",
        data = net_sent,
        label = 'sent'
        ))
    netdatasets.append(dict(
        backgroundColor="rgba(151,187,205,0.5)",
        borderColor = "rgba(151,187,205,1)",
        pointBackgroundColor = "rgba(151,187,205,1)",
        pointBorderColor = "#fff",
        data = net_recv,
        label = 'recv'
        ))
    netdata=dict(labels=labels,datasets=netdatasets)
    diskdatasets=[]
    diskdatasets.append(dict(
        backgroundColor="rgba(220,220,220,0.5)",
        borderColor = "rgba(220,220,220,1)",
        pointBackgroundColor = "rgba(220,220,220,1)",
        pointBorderColor = "#fff",
        data = disk_read,
        label = 'read'
        ))
    diskdatasets.append(dict(
        backgroundColor="rgba(151,187,205,0.5)",
        borderColor = "rgba(151,187,205,1)",
        pointBackgroundColor = "rgba(151,187,205,1)",
        pointBorderColor = "#fff",
        data = disk_write,
        label = 'write'
        ))
    diskdata=dict(labels=labels,datasets=diskdatasets)
    return JsonResponse(dict(cpu=cpudata,mem=memdata,net=netdata,disk=diskdata))

def time2str(t):
    return t.strftime('%H:%M:%S')
    #t.strftime('%Y-%m-%d %H:%M:%S')

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def HostLogCleanConfig(request,id,code):
    host = models.Host.objects.get(pk=id)
    configs = models.LogCleanConfig.objects.filter(host_id=id).all()
    return render(request,'HostManage/logCleanCfg.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def configDetail(request,id,cfg_id,code):
    host = models.Host.objects.get(pk=id)
    config = models.LogCleanConfig.objects.get(pk=cfg_id)
    if request.method=='POST':
        form = forms.LogCleanConfigEditForm(request.POST)
        if form.is_valid():
            cfg = form.save(commit=False)
            cfg.configName = config.configName
            cfg.host_id = id
            cfg.id = cfg_id
            cfg.sync=False
            cfg.save()
            logger.log(request,'编辑了主机%s(%s)的日志清理设置（%s）.'%(host.name,host.addr,cfg.configName))
            Channel('LogConfig').send({'host_id':id})
            return redirect('/HostManage/%s/LogCleanConfig/'%id)
    else:
        form = forms.LogCleanConfigEditForm(instance=config)
    return render(request,'HostManage/configdetail.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
def addconfig(request,id,code):
    host = models.Host.objects.get(pk=id)
    if request.method=='POST':
        form = forms.LogCleanConfigAddForm(request.POST)
        if form.is_valid():
            cfg = form.save(commit=False)
            cfg.host_id=id
            cfg.sync=False
            cfg.save()
            logger.log(request,'添加了主机%s(%s)的日志清理设置（%s）.'%(host.name,host.addr,cfg.configName))
            Channel('LogConfig').send({'host_id':id})
            return redirect('/HostManage/%s/LogCleanConfig/'%id)
    else:
        form = forms.LogCleanConfigAddForm()
    return render(request,'HostManage/addconfig.html',locals())

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
@csrf_exempt
def DeleteConfig(request,code):
    if request.method=='GET':
        return HttpResponse('404 Not Found')
    cfg_id = request.POST.get('cfg_id')
    cfg = models.LogCleanConfig.objects.get(pk=cfg_id)
    host = models.Host.objects.get(pk=cfg.host_id)
    logger.log(request,'删除了主机%s(%s)的日志清理设置（%s）.'%(host.name,host.addr,cfg.configName))
    cfg.isDel=True
    cfg.sync=False
    cfg.save()
    Channel('LogConfig').send({'host_id':cfg.host_id})
    return HttpResponse('')

@permission_required('SystemManage.access_to_Function',(Function,'name','code'))
@csrf_exempt
def addToTop(request,code):
    hostid = request.POST.get('hostid','')
    if not hostid:
        return JsonResponse(dict(ret=0))
    host = models.Host.objects.select_related().get(pk=hostid)
    if not host.isDel or user.is_superuser or (host.hostgroup and user in host.hostgroup.user.all()):
        host.onTopof.add(request.user)
        return JsonResponse(dict(ret=0))
    else:
        return JsonResponse(dict(ret=-1))

@csrf_exempt
def removeFromTop(request):
    hostid = request.POST.get('hostid','')
    host = models.Host.objects.select_related().get(pk=hostid)
    request.user.host_set.remove(host)
    return JsonResponse(dict(ret=0))