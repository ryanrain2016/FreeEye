import paramiko
from datetime import datetime
import os
from SystemManage.models import Log

class SSH:
    def __init__(self,hostname,port,username='root',password=''):
        self.hostname=hostname
        self.port = port
        self.username = username
        self.password = password
        self.connect()

    def connect(self):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(hostname = self.hostname,port=self.port,username=self.username, password=self.password)
        t=paramiko.Transport((self.hostname,self.port))
        t.connect(username=self.username,password=self.password)
        self._sftp = paramiko.SFTPClient.from_transport(t)

    def command(self,cmd):
        i,o,e = self._ssh.exec_command(cmd)
        return o.read()

    def exist_cmd(self,cmd):
        i,o,e = self._ssh.exec_command(cmd + '&& echo 1 || echo 0')
        out = o.readlines()
        return out[-1].strip()=='1'

    def putfile(self, file,remote_dir,on_exists='ba',cb=None):
        cwd = self._sftp.getcwd()
        self._sftp.chdir(remote_dir)
        files = self._sftp.listdir()
        filename = file.rsplit(os.sep,1)[-1]
        if filename in files:
            if on_exists=='ba':
                now = datetime.now()
                t = now.strftime('%Y%m%d%H%M%S')
                newname = '.'.join((filename,t,'bak'))
                self._sftp.rename(filename,newname)
            elif on_exists=='ov':
                try:
                    self._sftp.remove(filename)
                except IOError:
                    try:
                        self._sftp.rmdir(filename)
                    except:
                        pass
            else:
                if cwd:self._sftp.chdir(cwd)
                return
        self._sftp.put(file,filename,cb)
        if cwd:self._sftp.chdir(cwd)

    def writefile(self,content,file):
        f = self._sftp.open(file,'w')
        f.write(content)
        f.close()

    def readfile(self,file):
        f = self._sftp.open(file,'r')
        content=f.read()
        f.close()
        if type(content) is bytes:
            content=content.decode('utf-8')
        return content

    def close(self):
        self._sftp.close()
        self._ssh.close()

    def __del__(self):
        self.close()

class Logger:
    def log(self,request,do='',level='info'):
        log = Log(level=level,username=request.user.username,do=do)
        log.save()

    def debug(self,request,do=''):
        return self.log(request,do,'debug')

    def info(self,request,do=''):
        return self.log(request,do,'info')

    def warn(self,request,do=''):
        return self.log(request,do,'warn')

    def error(self,request,do=''):
        return self.log(request,do,'error')

    def fatal(self,request,do=''):
        return self.log(request,do,'fatal')