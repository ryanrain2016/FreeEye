from channels.routing import route, include
from . import consumers

routing = [
    route("websocket.connect",consumers.on_connect),
    route("websocket.receive",consumers.on_message),
    route("websocket.disconnect",consumers.on_disconnect),
]
