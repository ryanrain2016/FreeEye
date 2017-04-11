from channels.sessions import channel_session,http_session
from channels import Channel,Group
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import json
from HostManage import models
from FreeEye import utils

@channel_session_user_from_http
def ws_home_c(message):
    if message.user is not None:
        message.reply_channel.send({'accept':True})
        for host in message.user.host_set.all():
            Group('monitor_host_'+str(host.id)).add(message.reply_channel)
    
@channel_session_user
def ws_home(message):
    content = json.loads(message.content['text'])
    host = models.Host.objects.get(pk=content['hostid'])
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
def ws_home_d(message):
    for host in message.user.host_set.all():
        Group('monitor_host_'+str(host.id)).discard(message.reply_channel)