from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.conf import settings

from . import models
from . import forms
# Create your views here.

@csrf_exempt
@login_required
def alertManage(request):
    if request.method=='POST':
        name = request.POST.get('name','')
        _type = request.POST.get('_type','')
        factor = request.POST.get('factor','')
        threshold = request.POST.get('threshold','')
        receiver = request.POST.get('receiver','')
        if request.user.is_superuser:
            tableData = models.Alert.objects.all()
        else:
            tableData = models.Alert.objects.filter(createBy=request.user)
        if name:
            tableData = tableData.filter(name__icontains=name)
        if _type:
            tableData = tableData.filter(_type=_type)
        if factor:
            tableData = tableData.filter(factor=factor)
        if threshold:
            tableData = tableData.filter(threshold=threshold)
        if receiver:
            tableData = tableData.filter(receiver__icontains=receiver)

        paginator = Paginator(tableData,settings.ITEMS_PER_PAGE) #模板需要
        page = int(request.GET.get('page',1))                 #模板需要
        start = max(page-5,0)
        page_range = paginator.page_range[start:start+10]      #模板需要
        cur_page = paginator.page(page)                        #模板需要
        return render(request,'AlertManage/alerttablelist.html',locals())
    else:
        form = forms.AlertForm()
    return render(request,'AlertManage/alertList.html',locals())
