from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from api import serializers
from rest_framework import status



@api_view(['GET','POST'])
def admin_list(request):
    '''
    List all order, or create a server admin order.
    '''
    if request.method == "GET":
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))

        if page == 1:
            stat = page - 1
            end = page * limit
        else:
            stat = (page - 1) * limit
            end = page * limit
        # 直接展示表单
        queryset = User.objects.order_by('id').all()
        count = User.objects.order_by('id').all().count()
        serializer = serializers.UserSerializer(queryset, many=True)
        data = {"code": 0, "msg": '', "count": count, "data": serializer.data[stat:end]}
        return Response(data)


    if request.method == "POST":
        username = request.POST.get('username')
        role = request.POST.get('role')
        email = request.POST.get('email')
        infopass = request.POST.get('infopass')
        repass = request.POST.get('repass')

        if infopass and repass:

            if infopass != repass:
                return JsonResponse({"status": 400, "msg": '密码不一致'})

            try:
                User.objects.get(username=username)
                return JsonResponse({"user": username, "status": 400, "msg": '用户已存在'})

            except:

                if role == "general":
                    password = infopass
                    try:
                        User.objects.create_user(username, email=email, password=password)
                    except Exception as e:
                        return JsonResponse({"status": 400, "msg": e})

                    return JsonResponse({"status": 200, "msg": '增加成功'})

                elif role == "super":
                    password = infopass
                    try:
                        User.objects.create_superuser(username, email=email, password=password)
                    except Exception as e:
                        return JsonResponse({"status": 400, "msg": e})

                    return JsonResponse({"status": 200, "msg": '增加成功'})
        else:
            return JsonResponse({{"status": 400, "msg": '密码不能为空'}})





@api_view(["DELETE"])
def admin_detail(request):
    if request.method == "DELETE":
        ids = request.POST.get('ids')
        print(ids)

        if ids:
            try:
                #批量删除
                User.objects.extra(where=['id IN ('+ ids[:-1] +')']).delete()
                return JsonResponse({"status":200, "msg":"删除成功"})
            except:
                return JsonResponse({"status":400, "msg":"删除失败"})
        return JsonResponse({"status":400, "msg":"异常"})
