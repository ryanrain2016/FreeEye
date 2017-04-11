from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Host(models.Model):
    name = models.CharField(max_length=32)
    addr = models.CharField(max_length=128)
    port = models.IntegerField(default=22)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    remark = models.TextField(max_length=128,blank=True,default='')
    active = models.BooleanField(default=False)
    isDel = models.BooleanField(default=False)
    hostgroup = models.ForeignKey('SystemManage.HostGroup',on_delete=models.SET_NULL,blank=True,null=True,default=None)
    onTopof = models.ManyToManyField(User)
    createAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s -- %s'%(self.name,self.addr)


class HostInfo(models.Model):
    host = models.OneToOneField(Host)
    OS = models.CharField(max_length=64)
    cpu_version = models.CharField(max_length=128)
    cpu_thd_cnt = models.CharField(max_length=4)
    MAC = models.CharField(max_length=32)
    mem_total = models.CharField(max_length=16)
    kernal_version = models.CharField(max_length=128)

class HostStat(models.Model):
    host = models.ForeignKey(Host)
    cpu_sys = models.FloatField()
    cpu_usr = models.FloatField()
    cpu_idle = models.FloatField()
    mem_total = models.IntegerField()
    mem_used = models.IntegerField()
    mem_free = models.IntegerField()
    mem_avai = models.IntegerField()
    net_sent = models.IntegerField()
    net_recv = models.IntegerField()
    disk_write = models.IntegerField()
    disk_read = models.IntegerField()
    createAt = models.DateTimeField(auto_now_add=True)

class Application(models.Model):
    appName = models.CharField(max_length=32)
    cmdline = models.CharField(max_length=32)
    cmdArgs = models.CharField(max_length=128,null=True,blank=True)
    startCommand = models.CharField(max_length=256)
    stopCommand = models.CharField(max_length=256)
    restartCommand=models.CharField(max_length=256)

class HostAppliction(models.Model):
    OFF = 'OF'
    ON = 'ON'
    NI = 'NI'
    STATUS_CHOICES=(
        (OFF,'未启动'),
        (ON,'运行中'),
        (NI,'未安装'),
    )
    host = models.ForeignKey(Host)
    application = models.ForeignKey(Application)
    status = models.CharField(max_length=2,choices=STATUS_CHOICES,default=OFF)
    updateAt  = models.DateTimeField(auto_now=True)


class LogCleanConfig(models.Model):
    configName = models.CharField(max_length=32,verbose_name='配置名称')
    host_id = models.IntegerField(default=-1)
    LogPath = models.CharField(max_length=256,verbose_name='清理日志路径',help_text='单个目录一行')
    compress = models.BooleanField(default=False,verbose_name='Gzip压缩')
    copytruncate = models.BooleanField(default=True,verbose_name='截断打开的日志')
    create = models.BooleanField(default=True,verbose_name='完成后创建日志文件')
    mode_owner_group = models.CharField(max_length=64,default='',null=True,blank=True,verbose_name='创建文件的模式，属组',help_text='留空保持原来的模式，属组')
    delaycompress = models.BooleanField(default=False,verbose_name='是否延时压缩')
    ifempty = models.BooleanField(default=True,verbose_name='转储空日志')
    olddir = models.BooleanField(default=False,verbose_name='指定转储日志目录')
    directory = models.CharField(max_length=256,default='',null=True,blank=True,verbose_name='转储日志目录')
    missingok = models.BooleanField(default=True,verbose_name='日志不存在时不报错')
    prerotate = models.TextField(max_length=512,null=True,default='',blank=True,verbose_name='转储前执行脚本')
    postrotate = models.TextField(max_length=512,null=True,default='',blank=True,verbose_name='转储后执行脚本')
    cycle = models.CharField(max_length=8,choices=[
            ('daily','每天'),('weekly','每周'),('monthly','每月')
        ],default='weekly',verbose_name='转储周期')
    rotate = models.IntegerField(null=True,default=4,verbose_name='保留转储次数')
    size = models.CharField(max_length=16,verbose_name='转储大小阈值',default='20MB',help_text='可以指定 bytes (缺省)以及KB (sizek)或者MB (sizem)')
    sync = models.BooleanField(default=False)
    isDel = models.BooleanField(default=False)
    class Meta:
        unique_together = (('host_id', 'configName'),)

    def toConfigOnhtml(self):
        return self.toConfig().replace('\n','<br>')

    def toConfig(self):
        cfg = self.LogPath.replace('\r','') + ' {\n'
        cfg += 'compress\n' if self.compress else 'nocompress\n'
        cfg += 'copytruncate\n' if self.copytruncate else 'nocopytruncate\n'
        cfg += ('create '+ self.mode_owner_group + '\n') if self.create else 'nocreate\n'
        cfg += 'delaycompress\n' if self.delaycompress else 'nodelaycompress\n'
        cfg += 'ifempty\n' if self.ifempty else 'noifempty\n'
        cfg += ('olddir '+ self.directory + '\n') if self.olddir else 'noolddir\n'
        if self.prerotate.strip():
            cfg += 'prerotate\n'
            cfg += (self.prerotate.strip()+'\n')
            cfg += 'endscript\n'
        if self.postrotate.strip():
            cfg += 'postrotate\n'
            cfg += (self.postrotate.strip()+'\n')
            cfg += 'endscript\n'
        cfg += 'missingok\n' if self.missingok else 'nomissingok\n'
        cfg += (self.cycle + '\n')
        cfg += 'rotate %s\n'%self.rotate
        cfg += 'size %s\n'%self.size
        cfg += '}\n'
        return cfg

    @classmethod
    def fromCfg(cls,cfg,cfgName):
        lines = cfg.split('\n')
        prerotate = False
        postrotate = False
        logpath = True
        pre = []
        post = []
        path=[]
        for line in lines:
            line = line.strip()
            if line.startswith('#'):continue
            if logpath:
                if line.endswith('{'):
                    line = line.strip('{ ')
                    if line:path.append(line)
                    LogPath = '\n'.join(path)
                    inst = cls(configName=cfgName,LogPath=LogPath)
                    logpath=False
                    continue
                else:
                    path.append(line)
            if prerotate:
                pre.append(line)
                continue
            if postrotate:
                post.append(line)
                continue
            
            if line.startswith('compress'):
                inst.compress=True
                continue
            if line.startswith('uncompress'):
                inst.compress=False
                continue
            if line.startswith('copytruncate'):
                inst.copytruncate=True
                continue
            if line.startswith('nocopytruncate'):
                inst.copytruncate=False
                continue
            if line.startswith('create'):
                inst.create=True
                inst.mode_owner_group = line[7:]
                continue
            if line.startswith('nocreate'):
                inst.create=False
                continue
            if line.startswith('delaycompress'):
                inst.delaycompress=True
                continue
            if line.startswith('nodelaycompress'):
                inst.delaycompress=False
                continue
            if line.startswith('ifempty'):
                inst.ifempty=True
                continue
            if line.startswith('noifempty'):
                inst.ifempty=False
                continue
            if line.startswith('olddir'):
                inst.olddir=True
                inst.directory=line[7:]
                continue
            if line.startswith('noolddir'):
                inst.olddir=False
                continue
            if line.startswith('missingok'):
                inst.missingok=True
                continue
            if line.startswith('nomissingok'):
                inst.missingok=False
                continue
            if line.startswith('prerotate'):
                prerotate = True
                continue
            if line.startswith('postrotate'):
                postrotate = False
                continue
            if line.startswith('endscript'):
                if prerotate:
                    inst.prerotate='\n'.join(pre)
                    prerotate=False
                elif postrotate:
                    inst.postrotate='\n'.join(post)
                    postrotate=False
            if line in ('daily','weekly','monthly'):
                inst.cycle = line
                continue
            if line.startswith('rotate'):
                inst.rotate = int(line[7:].strip())
                continue
            if line.startswith('size'):
                inst.size = line[5:]
                continue
        return inst

