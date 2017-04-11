from channels.routing import route, include
from . import consumers

routing = [
    route("websocket.connect", consumers.ws_paramiko_proxy_c, path=r'^/paramiko_proxy/'),
    route("websocket.receive", consumers.ws_paramiko_proxy, path=r'^/paramiko_proxy/'),
    route("websocket.disconnect", consumers.ws_paramiko_proxy_d, path=r'^/paramiko_proxy/'),

    include('TaskManage.routings.routing',path=r'^/TaskManage/(?P<taskType>\w+)/(?P<id>\d+)/'),
    include('HostManage.routings.routing'),
    include('MainFrame.routings.routing'),
]
