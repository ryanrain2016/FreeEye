from channels.routing import route, include
from . import consumers

routing = [
    route('HostAdd',consumers.HostAdd),
    route('HostImport',consumers.HostImport),
    route("websocket.connect", consumers.ws_agent_c, path=r'^/agent/(?P<id>\d+)/'),
    route("websocket.receive", consumers.ws_agent, path=r'^/agent/(?P<id>\d+)/'),
    route("websocket.disconnect", consumers.ws_agent_d, path=r'^/agent/(?P<id>\d+)/'),

    route("websocket.connect", consumers.ws_user_c, path=r'^/user/(?P<id>\d+)/'),
    route("websocket.receive", consumers.ws_user, path=r'^/user/(?P<id>\d+)/'),
    route("websocket.disconnect", consumers.ws_user_d, path=r'^/user/(?P<id>\d+)/'),

    route("websocket.connect", consumers.ws_webshell_c, path=r'^/webshell/(?P<id>\d+)/'),
    route("websocket.receive", consumers.ws_webshell, path=r'^/webshell/(?P<id>\d+)/'),
    route("websocket.disconnect", consumers.ws_webshell_d, path=r'^/webshell/(?P<id>\d+)/'),

    route("LogConfig",consumers.LogConfig),
]