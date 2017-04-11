from channels.routing import route, include
from . import consumers

routing = [
    route("websocket.connect", consumers.ws_home_c, path=r'^/home/'),
    route("websocket.receive", consumers.ws_home, path=r'^/home/'),
    route("websocket.disconnect", consumers.ws_home_d, path=r'^/home/'),
]