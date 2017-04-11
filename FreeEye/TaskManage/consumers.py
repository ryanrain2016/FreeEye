from channels.sessions import channel_session,http_session
from channels import Channel
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import json,os,sys
from . import models 
from FreeEye import utils
from django.conf import settings
from FreeEye import utils
logger = utils.Logger()

@channel_session_user_from_http
def on_connect(message,taskType,id):
    message.reply_channel.send({"accept": True})
    #print("conncted",taskType,id)

@channel_session_user
def on_message(message,taskType,id):
    content = json.loads(message.content['text'])
    taskmodels = models.FileTask if taskType=='file' else models.CommandTask
    taskprogressmodels = models.FileTaskProgress if taskType=='file' else models.CommandTaskProgress
    task = taskmodels.objects.get(pk=id)
    taskprogress = taskprogressmodels.objects.filter(task=task)
    if content['action']=='execute':
        logger.info(message,'执行%s任务(%s)!'%('文件' if taskType=='file' else 'command',task.name))
        taskprogress = taskprogress.filter(is_start=False)
    elif content['action']=='reexecute':
        logger.info(message,'重新%s执行任务(%s)!'%('文件' if taskType=='file' else 'command',task.name))
        taskprogress = taskprogress.filter(is_start=True)
    elif content['action']=='singleexecute' or content['action']=='singlereexecute':
        taskprogress = taskprogress.filter(id=content['id'])
        logger.info(message,'%s%s执行任务(%s)!'%('重新' if 're' in content['action'] else '','文件' if taskType=='file' else 'command',task.name))
        taskprogress = taskprogress.filter(is_start=True)
    for tp in taskprogress:
        message.reply_channel.send({'text':json.dumps(dict(action='task',id=tp.id,status='开始'))})
        tp.is_start=True
        tp.save()
        host = tp.taskhost
        logger.info(message,'%s开始%s%s执行任务(%s)!'%(host.name,'重新' if 're' in content['action'] else '','文件' if taskType=='file' else 'command',task.name))
        try:
            ssh = utils.SSH(hostname=host.addr,
                port=host.port,
                username=host.username,
                password=host.password)
            logger.info(message,'%s完成%s%s执行任务(%s)!'%(host.name,'重新' if 're' in content['action'] else '','文件' if taskType=='file' else 'command',task.name))
        except:
            logger.info(message,'%s%s%s执行任务(%s)，出现错误!'%(host.name,'重新' if 're' in content['action'] else '','文件' if taskType=='file' else 'command',task.name))
            tp.result='错误'
            tp.save()
            continue

        if taskType=='file':
            try:
                ssh.putfile(os.path.join(settings.BASE_DIR,'taskfile',task.file),task.remote_file,task.on_exists)
            except:
                tp.result='错误'
                message.reply_channel.send({'text':json.dumps(dict(action='task',id=tp.id,status='完成',result='错误'))})
                tp.save()
                continue
            message.reply_channel.send({'text':json.dumps(dict(action='task',id=tp.id,status='完成',result='成功'))})
            tp.is_finish=True
            tp.result='成功'
            tp.save()
        elif taskType=='command':
            tp.is_start=True
            tp.save()
            try:
                ret = ssh.command(task.cmdline)
                if type(ret) is bytes:
                    ret = str(ret,'utf-8')
            except:
                tp.result='错误'
                message.reply_channel.send({'text':json.dumps(dict(action='task',id=tp.id,status='完成',result='错误'))})
                tp.save()
                continue
            message.reply_channel.send({'text':json.dumps(dict(action='task',id=tp.id,status='完成',result=ret))})
            tp.is_finish=True
            tp.result=ret
            tp.save()

   

@channel_session_user
def on_disconnect(message,taskType,id):
    pass

