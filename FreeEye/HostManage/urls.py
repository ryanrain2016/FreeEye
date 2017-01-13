from django.conf.urls import url
from . import views

urlpatterns=[
    url('^HostList/', views.hostList, name='hostlist'),
    url(r'^AddHost/',views.addHost,name='addhost'),
    url(r'^ImportHost',views.importHost,name='importhost'),
]
