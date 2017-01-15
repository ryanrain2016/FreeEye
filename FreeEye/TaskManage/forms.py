from django import forms
from . import models
class FileTaskForm(forms.ModelForm):
    class Meta:
        model = models.FileTask
        fields = ('name','file','remote_file','on_exists')
        widgets={
            'name':forms.CharField(attrs={'class':'form-control'}),
            'file':forms.CharField(attrs={'class':'form-control'}),
            'remote_file':forms.CharField(attrs={'class':'form-control'}),
            'on_exists':forms.Select(attrs={'class':'form-control'}),
        }
