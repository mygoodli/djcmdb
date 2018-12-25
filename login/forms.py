from django import forms
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class UserForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    captcha = CaptchaField(label='验证码')
    #widget=forms.PasswordInput用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框。