from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.mainframe, name='mainframe'),
    url(r'^login/', views.login, name='login'),
    url(r'^avatar_form/', views.avatar_form, name='avatar'),
    url(r'^profile_form/', views.profile_form, name='profile'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^index/', views.index, name='index'),
]
