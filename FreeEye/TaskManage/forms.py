from django import forms

from . import models

class FileTaskForm(forms.ModelForm):
    class Meta:
        model = models.FileTask
        fields = ('name','remote_file','on_exists')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'remote_file':forms.TextInput(attrs={'class':'form-control'}),
            'on_exists':forms.Select(attrs={'class':'form-control'}),
        }
        labels={
            'name':'任务名',
            'remote_file':'远程路径',
            'on_exists':'文件存在时',
        }

class FileTaskSearchForm(forms.Form):
    name = forms.CharField(max_length=32,required=False,label='任务名',widget=forms.TextInput(attrs={'class':'form-control'}))
    file = forms.CharField(max_length=256,required=False,label='文件',widget=forms.TextInput(attrs={'class':'form-control'}))
    remote_file = forms.CharField(max_length=256,required=False,label='远程文件',widget=forms.TextInput(attrs={'class':'form-control'}))
    on_exists = forms.ChoiceField(required=False,label='文件已存在时',choices=(('','----'),('ov','覆盖'),('ba','备份'),('sk','跳过')),widget=forms.Select(attrs={'class':'form-control'}))

class CommandTaskSearchForm(forms.Form):
    name = forms.CharField(max_length=32,required=False,label='任务名',widget=forms.TextInput(attrs={'class':'form-control'}))
    cmdline = forms.CharField(max_length=256,required=False,label='命令行',widget=forms.TextInput(attrs={'class':'form-control'}))

class CommandTaskForm(forms.ModelForm):
    class Meta:
        model = models.CommandTask
        fields = ('name','cmdline')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'cmdline':forms.TextInput(attrs={'class':'form-control'}),
        }
        labels={
            'name':'任务名',
            'cmdline':'命令行',
        }
