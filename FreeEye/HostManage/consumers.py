from channels.sessions import channel_session,http_session
from channels import Channel
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

from django.shortcuts import render_to_response
from django.conf import settings
from FreeEye import utils
from . import models

try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:  # pragma: no cover
    from django.contrib.sites.models import get_current_site

#protocol = 'https' if request.is_secure() else 'http'
#site = get_current_site(request)
def InstallAgent(message):  #
    kw = message.content
    site = kw.get('site',settings.SITE)
    ws_protocol = kw.get('ws_protocol',settings.WS_PROTOCOL)
    id = kw.get('id',None)
    if id is None:return
    host = Host.objects.get(pk=id)
    ssh = utils.SSH(hostname=host.addr,port=host.port,username=host.username,password=host.password)
    ssh.command('mkdir /usr/local/FreeEye')
    configfile = os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent.conf')
    config = open(configfile).read()%locals()
    ssh.writefile(config,'/usr/local/FreeEye/FreeEye_Agent.conf')
    ssh.putfile(os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent_py2.py','/usr/local/FreeEye/')
    ssh.putfile(os.path.join(settings.BASE_DIR,'Agent','FreeEye_Agent','/etc/init.d/')
    ssh.command('chmod 755 /etc/init.d/FreeEye_Agent')
