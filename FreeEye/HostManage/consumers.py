from channels.sessions import channel_session,http_session
from channels import Channel
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from django.shortcuts import render_to_response
from django.conf import settings
from FreeEye.utils import *
from . import models

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

#protocol = 'https' if request.is_secure() else 'http'
#site = get_current_site(request)
def InstallAgent(message):  #
    kw = message.content
    site = kw.get('site','')
    ws_protocol = kw.get('ws_protocol','ws')
    id = kw.get('id',None)
    if id is None:return
    host = Host.objects.get(pk=id)
    ssh = getSSH(hostname=host.addr,port=host.port,username=host.username,password=host.password)
    SShCommand(ssh,'mkdir /usr/local/FreeEye')
    configfile = os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent.conf')
    config = open(configfile).read()%locals()
    SSHFileWrite(ssh,config,'/usr/local/FreeEye/FreeEye_Agent.conf')
    SSHFilePut(ssh,os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent_py2.py','/usr/local/FreeEye')
    
