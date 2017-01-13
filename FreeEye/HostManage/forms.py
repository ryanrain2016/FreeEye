from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models
import SystemManage

class HostSearchForm(forms.Form):
    name = forms.CharField(max_length=20,required=False,label='主机名称',widget=forms.TextInput(attrs={'class': 'form-control'}))
    addr = forms.CharField(max_length=20,required=False,label='主机地址',widget=forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.IntegerField(required=False,label='ssh端口',widget=forms.TextInput(attrs={'class': 'form-control'}))
    group = forms.ModelChoiceField(queryset=None,required=False,label='主机组',widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self,*args,user=None,**kwargs):
        super(HostSearchForm, self).__init__(*args,**kwargs)
        if user is not None:
            groups = SystemManage.models.HostGroup.objects.filter(user=user)
            self.fields['group'].queryset = groups

class HostAddForm(forms.ModelForm):
    name = forms.CharField(max_length=32,label='主机名称：',widget=forms.TextInput(attrs={'class': 'form-control'}))
    addr = forms.CharField(max_length=128,label='主机地址：',widget=forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.IntegerField(label='主机端口：',widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='主机用户名：',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=64,label='主机密码：',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remark = forms.CharField(max_length=128,required=False,label='备注：',widget=forms.TextInput(attrs={'class': 'form-control'}))
    class Meta:
        model = models.Host
        fields = ['name', 'addr', 'port','username', 'password','remark']
