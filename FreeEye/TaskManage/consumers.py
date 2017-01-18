from channels.sessions import channel_session,http_session
from channels import Channel
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http

#@channel_session_user_from_http
def on_connect(message,taskType,id):
    message.reply_channel.send({"accept": True})
    print("conncted",taskType,id)
