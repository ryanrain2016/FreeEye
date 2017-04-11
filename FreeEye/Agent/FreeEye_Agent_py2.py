import websocket
from  ConfigParser import ConfigParser,NoSectionError,NoOptionError
import thread
import time
import logging
import multiprocessing
import os,sys
import psutil
import json
import threading

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='%s.log'%(__file__.rsplit('.',1)[0]),
    filemode='a')

def singleton(cls):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return _singleton

@singleton
class Settings(object):
    def __init__(self):
        self._config = '/usr/local/FreeEye/FreeEye_Agent.conf'
        self.cp = ConfigParser()
        self.cp.read(self._config)

    def reload(self):
        self.cp.read(self._config)

    def __getattribute__(self,section_key,default=None):
        try:
            return object.__getattribute__(self, section_key)
        except:
            pass
        section, key = section_key.split('_', 1)
        try:
            value = self.cp.get(section, key)
        except (NoSectionError, NoOptionError):
            logging.info('Config [%s]->%s not found,use default[%s] instead!'
                %(section,key,default))
            value = default
        return value

    def __getattr__(self,section_key,default=None):
        try:
            return object.__getattr__(self, section_key)
        except:
            pass
        section, key = section_key.split('_', 1)
        try:
            value = self.cp.get(section, key)
        except (NoSectionError, NoOptionError):
            logging.info('Config [%s]->%s not found,use default[%s] instead!'
                %(section,key,default))
            value = default
        return value

class Performance(object):
    def __init__(self):
        self.ps = psutil

    @property
    def stats(self):
        stats = self.ps.cpu_times_percent()
        mem = self.ps.virtual_memory()
        return dict(
            cpu_usr = stats.user,
            cpu_sys = stats.system,
            cpu_idle = stats.idle,
            mem_total = mem.total/1024/1024,
            mem_avai = mem.available/1024/1024,
            mem_free = mem.free/1024/1024,
            mem_used = mem.used/1024/1024
        )

    @property
    def counters(self):
        net = self.ps.net_io_counters()
        disk = self.ps.disk_io_counters()
        return dict(
            net_sent = net.bytes_sent/1024.0,
            net_recv = net.bytes_recv/1024.0,
            disk_read = disk.read_bytes/1024.0,
            disk_write = disk.write_bytes/1204.0
        )

    def parse_counters(self, counters1, counters2, interval):
        d = {}
        for k in counters1:
            d[k] = (counters2[k]-counters1[k])/interval
        return d
        #return {k:(counters2[k]-counters1[k])/interval for k in counters1}

class DataCollector(object):
    def __init__(self):
        self.infocmd_table = {
            'cpu_version':"cat /proc/cpuinfo | grep 'model name' | awk '{ print $4,$5,$6,$7,$8,$9,$10,$11}'",
            'cpu_thd_cnt':"cat /proc/cpuinfo | grep 'model name' | wc -l",
            'OS':'uname -o',
            'MAC':["ifconfig | grep ether | awk '{print $2}'","ifconfig | grep HWaddr | awk '{print $5}'"],
            'mem_total':"free | grep Mem | awk '{print $2}'",
            'kernal_version':"uname -rv",
        }

    def getInfo(self,info):
        cmd = self.infocmd_table.get(info,None)
        if cmd is None:raise KeyError('Info name %s Error'%info)
        if type(cmd) is list:
            for c in cmd:
                p = os.popen(c).read()
                if p.strip():
                    return p.strip()
        else:
            p = os.popen(cmd)
            return p.read().strip()

    def getAllInfo(self):
        infos={}
        for info in self.infocmd_table:
            infos[info] = self.getInfo(info)
        return infos

class ApplicationMonitor(object):
    def __init__(self):
        self.table = {
            'apache':'ps -ef | grep httpd | grep -v grep | wc -l',
            'nginx':'ps -ef | grep nginx | grep -v grep | wc -l',
            'mysql':'ps -ef | grep mysqld | grep -v grep | wc -l',
            'tomcat':'ps -ef | grep tomcat | grep -v grep | wc -l'
        }

    def getstatus(self):
        status = {}
        for k in self.table:
            p = os.popen(self.table[k])
            p = p.read()
            if p.strip()=='0':
                status[k]='OF'
            else:
                status[k]='ON'
        return status

def on_message(ws, message):
    logging.info('recv: %s'%message)

def on_error(ws, error):
    logging.error('error: %s'%error)

def on_close(ws):
    logging.warn('Connection closed!')

def getStat(ws):
    interval = int(Settings().monitor_interval)
    p = Performance()
    am = ApplicationMonitor()
    while True:
        c1 = p.counters
        time.sleep(interval)
        c2 = p.counters
        stats = p.stats
        c = p.parse_counters(c1,c2,interval)
        stats.update(c)
        statMessage = dict(type='stat',id=Settings().monitor_agentid,data=stats,appdata=am.getstatus())
        ws.send(json.dumps(statMessage))


def getInfo(ws):
    interval = 24*3600
    dc = DataCollector()
    while True:
        infos = dc.getAllInfo()
        infoMessage = dict(type='info',id=Settings().monitor_agentid,data=infos)
        ws.send(json.dumps(infoMessage))
        time.sleep(interval)

def on_open(ws):
    t1 = threading.Thread(target=getStat,args=(ws,))
    t1.setDaemon(True)
    t1.start()
    t2 = threading.Thread(target=getInfo,args=(ws,))
    t2.setDaemon(True)
    t2.start()

def main():
    #websocket.enableTrace(True)
    ws = websocket.WebSocketApp(Settings().server_ws_url+Settings().monitor_agentid+'/',
        on_message = on_message,
        on_error = on_error,
        on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def deamon():
    while True:
        p = multiprocessing.Process(target=main)
        p.start()
        p.join()
        time.sleep(0.1)

def createDeamon(func,*args,**kwargs):
    try:
        if os.fork()>0:os._exit(0)
    except OSError as e:
        logging.error('Fork failed,you should use agent only on platform that support os.fork!')
        os._exit(1)
    os.chdir('/')
    os.setsid()
    os.umask(0)
    try:
        pid = os.fork()
        if pid > 0:
            #print('Daemon PID %d'%pid)
            os._exit(0)
    except OSError as e:
        logging.error('Fork failed,you should use agent only on platform that support os.fork!')
        os._exit(1)
    sys.stdout.flush()
    sys.stderr.flush()
    si = file("/dev/null", 'r')
    so = file("/dev/null", 'a+')
    se = file("/dev/null", 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
    func(*args,**kwargs)

if __name__ == "__main__":
    createDeamon(deamon)
