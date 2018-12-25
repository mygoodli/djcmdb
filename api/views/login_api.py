from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import auth
from django.shortcuts import Http404
from django.contrib.auth.decorators import login_required
from login import forms
from django.http import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt ,csrf_protect
import datetime
from django.contrib.auth.models import Permission, User
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.settings import api_settings
from mycmdb.view import obtain_expiring_auth_token

@csrf_exempt
#@api_view(['POST'])
def login_api(request):
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

                    #obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
                    print('ok')
                    return JsonResponse({"status":200})
                else:
                    message = "密码不正确！"
                    return JsonResponse({"status": 400, "msg": message})
            except User.DoesNotExist:
                message = "用户不存在！"
            print(1)
            return JsonResponse({"status": 400,"msg":message})
            #return render(request, 'login/login.html', locals())
        return JsonResponse({"status": 400, "msg": message})



def logout_out(request):
    #点击退出的时候，清空会话
    auth.logout(request)
    #在顶部额外导入了redirect，用于logout后，页面重定向到‘index’首页,def login...
    return redirect("login")