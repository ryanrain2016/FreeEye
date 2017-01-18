from channels.sessions import channel_session,http_session
from channels import Channel

import json
import os
import paramiko
import threading, time, re

# from shell import models

def terminal2html(data):
    data = data.replace('\n','<br>').replace(' ','&nbsp;').replace('\033[K','').replace('\033[m','\033[0m')
    data = re.sub(r'(\033\[((\d{1,2};?)+)m)', deal_term, data)
    return data

def deal_term(term):
    colors = ['black','red','green','yellow','blue','purple','green','white']
    s = term.groups()[1]
    if s=='0':
        return '</font>'
    modes = s.split(';')
    style=''
    for mode in modes:
        mode = int(mode)
        if 30<=mode<=37:
            style+='color:%s;'%colors[mode-30]
        elif 40<=mode<=47:
            style+='background:%s;'%colors[mode-40]
    return '<font style="%s">'%style

def ws_paramiko_proxy_c(message):
    channel_name = message.reply_channel.name
    models.ParamikoProxyChannel.objects.all().delete()
    models.ParamikoProxyChannel(channel_name=channel_name).save()

def ws_paramiko_proxy(message):
    text = message.content['text']
    msg = json.loads(text)
    sessionid = msg['sessionid']
    ip = msg['ip']
    user_channel = models.UserChannel.objects.filter(session_id=sessionid).all()[0].channel_name
    Channel(user_channel).send({'text':json.dumps(dict(
        html = '<span>%s</span>'%terminal2html(msg['data'])
    ))})

def ws_paramiko_proxy_d(message):
    channel_name = message.reply_channel.name
    models.ParamikoProxyChannel.objects.filter(channel_name=channel_name).delete()

@http_session
@channel_session
def ws_connect(message):
    message.channel_session['session_key']=message.http_session.session_key
    session_id = message.channel_session['session_key']
    channel_name = message.reply_channel.name
    models.UserChannel.objects.filter(session_id=session_id).delete()
    models.UserChannel(session_id=session_id,channel_name=channel_name).save()

@channel_session
def ws_message(message):
    session_id = message.channel_session['session_key']
    ip = '172.19.3.72'
    text = message.content['text']
    key = message.channel_session['session_key']
    cmd = json.loads(text)
    command = cmd['cmd']
    paramiko_proxy_channel = models.ParamikoProxyChannel.objects.all()[0].channel_name
    Channel(paramiko_proxy_channel).send({'text':json.dumps(dict(
        cmd='stream',
        sessionid=session_id,
        ip=ip,
        data=command,
    ))})

@channel_session
def ws_disconnect(message):
    session_id = message.channel_session['session_key']
    models.UserChannel.objects.filter(session_id=session_id).delete()
