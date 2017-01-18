from channels.routing import route, include
from . import consumers

routing = [
    route("websocket.connect",consumers.on_connect)
]
