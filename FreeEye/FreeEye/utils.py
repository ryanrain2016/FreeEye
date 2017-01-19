import paramiko
from datetime import datetime


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
        self._ssh.connect(hostname = self.hostname,port=self.port,username=self.username, self.password=password)
        self._sftp = paramiko.SFTPClient.from_transport(self._ssh)

    def command(self,cmdline):
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
        if file in files:
            if on_exists=='ba':
                now = datetime.now()
                t = now.strftime('%Y%m%d%H%M%S')
                newname = '.'.join((file,t,'bak'))
                self._sftp.rename(file,newname)
            elif on_exists=='ov':
                try:
                    self._sftp.remove(file)
                except IOError:
                    self._sftp.rmdir(file)
            else:
                if cwd:self._sftp.chdir(cwd)
                return
        self._sftp.put(file,file,cb)
        if cwd:self._sftp.chdir(cwd)

    def writefile(self,content,file):
        f = self._sftp.open(file,'w')
        f.write(content)
        f.close()

    def SSHFileRead(self,file):
        f = self._sftp.open(file,'r')
        content=f.read()
        f.close()
        return content

    def close(self):
        self._sftp.close()
        self._ssh.close()

    def __del__(self):
        self.close()
