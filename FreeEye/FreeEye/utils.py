import paramiko
from datetime import datetime

def getSSH(hostname,port,username='root',password=''):
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname = hostname,port=port,username=username, password=password)
    return s

def SShCommand(ssh,cmd):
    i,o,e = ssh.exec_command(cmd)
    return o.read()

def SSHFilePut(ssh,file,remote_dir,on_exists='ba',cb=None): #ba:备份，ov:覆盖，'sk':跳过
    sftp = paramiko.SFTPClient.from_transport(ssh)
    cwd = sftp.getcwd()
    sftp.chdir(remote_dir)
    files = sftp.listdir()
    if file in files:
        if on_exists=='ba':
            now = datetime.now()
            t = now.strftime('%Y%m%d%H%M%S')
            newname = '.'.join((file,t,'bak'))
            sftp.rename(file,newname)
        elif on_exists=='ov':
            try:
                sftp.remove(file)
            except IOError:
                sftp.rmdir(file)
        else:
            return
    sftp.put(file,file,cb)
    if cwd:sftp.chdir(cwd)
    sftp.close()

def SSHFileWrite(ssh,content,file):
    sftp = paramiko.SFTPClient.from_transport(ssh)
    f = sftp.open(file,'w')
    f.write(content)
    f.close()
    sftp.close()

def SSHFileRead(ssh,file):
    sftp = paramiko.SFTPClient.from_transport(ssh)
    f = sftp.open(file,'r')
    content=f.read()
    f.close()
    sftp.close()
    return content
