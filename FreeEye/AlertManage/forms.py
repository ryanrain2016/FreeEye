from django import forms
from . import models

class AlertForm(forms.ModelForm):
    class Meta:
        model = models.Alert
        fields = ('name','_type','factor','threshold','receiver','alertContent')
        labels = {
            'name':'名字',
            '_type':'告警类型',
            'factor':'告警参数',
            'threshold':'告警阈值',
            'receiver':'接受者',
            'alertContent':'告警内容',
        }
        widgits={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            '_type':forms.Select(attrs={'class':'form-control'}),
            'factor':forms.Select(attrs={'class':'form-control'}),
            'threshold':forms.TextInput(attrs={'class':'form-control'}),
            'receiver':forms.TextInput(attrs={'class':'form-control'}),
            'alertContent':forms.TextInput(attrs={'class':'form-control'}),
        }
