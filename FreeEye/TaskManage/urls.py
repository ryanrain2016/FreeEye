from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^CommandDispatch/',views.commandTask,name='commandtask'),
    url(r'^FileDispatch/',views.fileTask,name='filetask'),
]
