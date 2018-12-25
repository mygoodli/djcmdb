from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .import forms
from django.contrib.auth.models import Permission, User
from django.contrib import auth
from django.shortcuts import redirect,render_to_response
import datetime

# Create your views here.

#@login_required修饰器修饰的view函数会先通过session key检查是否登录, 已登录用户可以正常的执行操作
#未登录用户将被重定向到login_url指定的位置。若未指定login_url参数, 则重定向到settings.LOGIN_URL。

@login_required
def index(request):
    if request.method == "GET":
        pass
    return render(request,'index.html',locals())



def login(request):
    if request.method == "GET":
        login_form = forms.UserForm()

        return render(request,'login/login.html',locals())

    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                User.objects.get(username=username)
                user = auth.authenticate(username=username, password=password)
                if user is not None and user.is_active:
                    auth.login(request, user)
                    return render_to_response('index.html',locals())
                else:
                    message = "密码不正确或用户未激活！"
                return render(request, 'login/login.html', locals())
            except User.DoesNotExist:
                message = "用户不存在"
                return render(request,'login/login.html',locals())

    login_form = forms.UserForm()
    return render(request, 'login/login.html', locals())


def logout_out(request):
    #点击退出的时候，清空会话
    auth.logout(request)
    #在顶部额外导入了redirect，用于logout后，页面重定向到‘index’首页,def login...
    return redirect('login')


@login_required
def welcome(request):
    nowdatetime = datetime.datetime.now()

    return render(request,'welcome.html',{'nowdatetime':nowdatetime})

def error_show(request):
    '''
    返回错误页面
    :param request:
    :return:
    '''
    pass
    return render(request,'error.html')