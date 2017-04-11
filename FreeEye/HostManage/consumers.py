from channels.sessions import channel_session,http_session
from channels import Channel,Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from django.shortcuts import render_to_response
from django.conf import settings
from FreeEye import utils
from . import models
import xlrd

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

import os,json,time

#protocol = 'https' if request.is_secure() else 'http'
#site = get_current_site(request)
def InstallAgent(site,ws_protocol,id):  #
    if id is None:return
    host = models.Host.objects.get(pk=id)
    ssh = utils.SSH(hostname=host.addr,port=host.port,username=host.username,password=host.password)
    if not ssh.exist_cmd('yum -y install net-tools'):return 
    ssh.command('mkdir /usr/local/FreeEye')
    configfile = os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent.conf')
    config = open(configfile).read()%locals()
    ssh.writefile(config,'/usr/local/FreeEye/FreeEye_Agent.conf')
    ssh.putfile(os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent_py2.py'),'/usr/local/FreeEye/',on_exists='ov')
    ssh.putfile(os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent'),'/etc/init.d/',on_exists='ov')
    ssh.command('chmod 755 /etc/init.d/FreeEye_Agent')
    if not ssh.exist_cmd('pip'):
        ssh.command('yum install -y python-setuptools python-devel')
        ssh.command('easy_install pip')
    if not ssh.exist_cmd('gcc'):
        ssh.command('yum install -y gcc')
    ssh.command('pip install websocket-client psutil')
    ssh.command('service FreeEye_Agent start')
    ssh.close()
    SyncConfig(id)

def SyncConfig(id):
    host = models.Host.objects.get(pk=id)
    ssh = utils.SSH(hostname=host.addr,port=host.port,username=host.username,password=host.password)
    cfgs = ssh._sftp.listdir('/etc/logrotate.d/')
    for cfg in cfgs:
        inst,create = models.LogCleanConfig.objects.get_or_create(configName = cfg,host_id=id)
        config = ssh.readfile('/etc/logrotate.d/'+cfg)
        cfgconfig = models.LogCleanConfig.fromCfg(config,cfg)
        cfgconfig.host_id=id
        cfgconfig.id=inst.id
        cfgconfig.sync=True
        cfgconfig.save()


def HostAdd(message):
    kw = message.content
    site = kw.get('site',settings.SITE)
    ws_protocol = kw.get('ws_protocol',settings.WS_PROTOCOL)
    id = kw.get('id',None)
    InstallAgent(site,ws_protocol,id)

def HostImport(message):
    kw = message.content
    file = kw.get('file','')
    site = kw.get('site',settings.SITE)
    ws_protocol = kw.get('ws_protocol',settings.WS_PROTOCOL)
    if not file.endswith('.xls') and not file.endswith('.xlsx'):
        return
    data = xlrd.open_workbook(file)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    for i in range(nrows):
        cols = table.row_values(i)
        host = models.Host(name=cols[0],addr=cols[1],port=cols[2],username=cols[3],password=cols[4],remark=cols[5])
        try:
            host.save()
            InstallAgent(site,ws_protocol,host.id)
        except:
            continue

def ws_agent_c(message,id):
    host = models.Host.objects.get(pk=id)
    if host.isDel:
        message.reply_channel.send({'accept':False})
        return
    host.active=True
    host.save()
    data = json.dumps(dict(id=id,action='info',active=True))
    Group('monitor_host_'+str(id)).send({'text':data})
    message.reply_channel.send({'accept':True})

def ws_agent(message,id):
    content = json.loads(message.content['text'])
    if content['type']=='info':
        info = models.HostInfo.objects.get_or_create(host_id = id)[0]
        info.save()
        models.HostInfo(host_id=id,**content['data'],id=info.id).save()
    elif content['type']=='stat':
        stat = models.HostStat(host_id = id,**content['data'])
        stat.save()
        content['createAt']=stat.createAt.strftime('%H:%M:%S')
        if 'appdata' in content:
            for k in content['appdata']:
                app = models.Application.objects.filter(appName=k).all()[0]
                hostapp = models.HostAppliction.objects.get_or_create(host_id=id,application=app)[0]
                hostapp.status=content['appdata'][k]
                hostapp.save()
        Group('monitor_host_'+id).send({'text':json.dumps(content)})
        
def ws_agent_d(message,id):
    host = models.Host.objects.get(pk=id)
    host.active=False
    host.save()
    data = json.dumps(dict(id=id,type='info',active=False))
    Group('monitor_host_'+str(id)).send({'text':data})

@channel_session_user_from_http
def ws_user_c(message,id):
    user = message.user
    host = models.Host.objects.get(pk=id)
    if not host.isDel or user.is_superuser or (host.hostgroup and user in host.hostgroup.user.all()):
        message.reply_channel.send({'accept':True})
        Group('monitor_host_'+id).add(message.reply_channel)
    else:
        message.reply_channel.send({'accept':False})

@channel_session_user
def ws_user(message,id):
    content = json.loads(message.content['text'])
    host = models.Host.objects.get(pk=id)
    ssh = utils.SSH(hostname=host.addr,port=host.port,username=host.username,password=host.password)
    app = content['appName']
    app = models.Application.objects.filter(appName=app).all()[0]
    if content['status']:
        print(app.startCommand)
        ssh.command(app.startCommand)
    else:
        print(app.stopCommand)
        ssh.command(app.stopCommand)

@channel_session_user
def ws_user_d(message,id):
    Group('monitor_host_'+id).discard(message.reply_channel)


@channel_session_user_from_http
def ws_webshell_c(message,id):
    user = message.user
    host = models.Host.objects.get(pk=id)
    if not host.isDel or host.hostgroup and user in host.hostgroup.user.all() or user.is_superuser:
        message.reply_channel.send({'accept':True})
    else:
        message.reply_channel.send({'accept':False})


@channel_session_user
def ws_webshell(message,id):
    content = json.loads(message.content['text'])
    msg = dict(cmd='stream',data=content['cmd'],id=id,reply_channel=message.reply_channel.name)
    Group('paramiko').send({'text':json.dumps(msg)})

@channel_session_user
def ws_webshell_d(message,id):
    msg = dict(cmd='discard',reply_channel=message.reply_channel.name)
    Group('paramiko').send({'text':json.dumps(msg)})

def LogConfig(message):
    kw = message.content
    host_id = kw.get('host_id')
    host = models.Host.objects.get(pk=host_id)
    cfgs = models.LogCleanConfig.objects.filter(host_id=host_id).all()
    ssh = utils.SSH(hostname=host.addr,port=host.port,username=host.username,password=host.password)
    for cfg in cfgs:
        if cfg.isDel:
            ssh.command('rm -rf /etc/logrotate.d/' + cfg.configName)
            cfg.delete()
        else:
            ssh.writefile(cfg.toConfig(),'/etc/logrotate.d/' + cfg.configName)
            cfg.sync=True
            cfg.save()