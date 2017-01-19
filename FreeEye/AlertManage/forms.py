from django import forms
from . import models

class AlertForm(models.ModelForm):
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
            'name':models.TextInput(attrs={'class':'form-control'}),
            '_type':models.Select(attrs={'class':'form-control'}),
            'factor':models.Select(attrs={'class':'form-control'}),
            'threshold':models.TextInput(attrs={'class':'form-control'}),
            'receiver':models.TextInput(attrs={'class':'form-control'}),
            'alertContent':models.TextArea(attrs={'class':'form-control'}),
        }
