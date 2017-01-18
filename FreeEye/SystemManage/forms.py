from django import forms
import re
class UserForm(forms.Form):
    username = forms.CharField(max_length=16,label='用户名',widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=20,label='密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(max_length=20,label='确认密码',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password_1 = cleaned_data.get("password")
        password_2 = cleaned_data.get("password1")
        if password_1 != password_2:
            raise forms.ValidationError('密码不一致!')
        if len(password_1)<8 or len(password_1)>20:
            raise forms.ValidationError('密码长度在8-20之间!')
        if re.match(r'[a-zA-Z0-9~!@#$%^&\*\(\)\?\\\[\]\{\}]{8,20}',password_1) is None:
            raise forms.ValidationError('密码不能包含特殊字符！')
