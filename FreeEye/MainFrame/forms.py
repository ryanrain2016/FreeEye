from django import forms
from .models import Profile
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import re

def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')

class ProfileForm(forms.ModelForm):
    phone = forms.CharField(label=_("手机号码"), validators=[mobile_validate],required=False)
    class Meta:
        model = Profile
        fields=['phone','email','address']
        labels = {
            'phone':_("电话号码"),
            'email':_("电子邮件"),
            'address':_("地址"),
        }
