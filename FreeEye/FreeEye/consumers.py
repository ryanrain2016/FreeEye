from channels.sessions import channel_session,http_session
from channels import Channel,Group

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
    Group('paramiko').add(message.reply_channel)
    message.reply_channel.send({'accept':True})
    

def ws_paramiko_proxy(message):
    text = message.content['text']
    msg = json.loads(text)
    key = msg['reply_channel']
    data = msg['data']
    Channel(key).send({'text':json.dumps(dict(
        html = '<span>%s</span>'%terminal2html(msg['data'])
    ))})

def ws_paramiko_proxy_d(message):
    Group('paramiko').discard(message.reply_channel)

