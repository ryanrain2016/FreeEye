from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.
from .models import Profile, Menu
from .forms import ProfileForm
import json,os,re
# Create your views here.
def jsonify(**kw):
    return HttpResponse(json.dumps(dict(**kw)),content_type='json/application')

@login_required
def mainframe(request):
    menues = Menu.objects.all()
    return render(request,'mainframe.html',locals())

def login(request):
    if request.method=='POST' and request.POST:
        u = authenticate(username=request.POST.get('username',None),
            password=request.POST.get('password',None))
        if u is not None:
            if u.is_active:
                _login(request, u)
                next = request.GET.get('next',settings.LOGIN_DIRECT)
                return redirect(next)
            else:
                messages.error(request, '用户未激活！')
        else:
            messages.error(request, '用户名或者密码错误！')
    return render(request,'login.html',locals())

def logout(request):
    _logout(request)
    return redirect('/')

@login_required
@csrf_exempt
def avatar_form(request):
    if request.method=='GET':
        return render(request,'MainFrame/form_avatar.html')
    avatar = request.FILES.get('avatar',None)
    if avatar is None:return jsonify(ret=-1)
    username = request.user.username
    filename = os.path.join(settings.MEDIA_ROOT,'avatar',username+'.png')
    with open(filename, 'wb+') as destination:
        for chunk in avatar.chunks():
            destination.write(chunk)
    url = settings.MEDIA_URL + 'avatar/'+username+'.png'
    user = request.user
    if hasattr(user,'profile'):
        p = user.profile
        p.avatar=url
        p.save()
    else:
        p = Profile(avatar=url)
        p.user = user
        p.save()
    return jsonify(ret=0,avatar=p.avatar)

@login_required
def profile_form(request):
    u = request.user
    if hasattr(u,'profile'):
        p = u.profile
    else:
        p = Profile()
    if request.method == 'GET':
        form = ProfileForm(instance=p)
        return render(request,'MainFrame/form_profile.html',locals())
    else:
        p.user = u
        form = ProfileForm(request.POST,instance=p)
        if form.is_valid():
            form.save()
        return render(request,'MainFrame/form_profile.html',locals())

def index(request):
    return HttpResponse('这是临时主页内容')
