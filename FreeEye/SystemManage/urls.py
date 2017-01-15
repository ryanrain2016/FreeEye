from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^GroupManage/',views.hostGroupList,name='hostgrouplist'),
    url(r'^AddHostGroup/',views.addHostGroup,name='addhostgroup'),
]
