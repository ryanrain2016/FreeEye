from channels.routing import route, include
from . import consumers

routing = [
    route("websocket.connect", consumers.ws_paramiko_proxy_c, path=r'^/paramiko_proxy/'),
    route("websocket.receive", consumers.ws_paramiko_proxy, path=r'^/paramiko_proxy/'),
    route("websocket.disconnect", consumers.ws_paramiko_proxy_d, path=r'^/paramiko_proxy/'),
    include('TaskManage.routings.routing',path=r'^/TaskManage/(?P<taskType>\w+)/(?P<id>\d+)/'),
    # route("websocket.connect", consumers.ws_connect),        #当WebSocket请求连接上时调用consumers.ws_connect函数
    # route("websocket.receive", consumers.ws_message),        #当WebSocket请求发来消息时。。。
    # route("websocket.disconnect", consumers.ws_disconnect),    #当WebSocket请求断开连接时。。。

]
