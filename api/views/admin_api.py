from django.contrib.auth.models import User,Permission,Group
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from api import serializers
from rest_framework import status
import json


@api_view(['GET','POST'])
def admin_list(request):
    '''
    List all order, or create a server admin order.
    获取，新建管理员
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





@api_view(["DELETE","PUT"])
def admin_detail(request):
    '''
    Retrieve, update or delete a admin instance.
    检索、更新或删除管理员实例。
    '''
    ids = request.POST.get('ids')
    id = request.POST.get('id')

    if request.method == "DELETE":

        print(id)
        print(ids)

        if ids:
            try:
                #批量删除
                User.objects.extra(where=['id IN ('+ ids[:-1] +')']).delete()
                return JsonResponse({"status":200, "msg":"删除成功"})
            except:
                return JsonResponse({"status":400, "msg":"删除失败"})
        else:
            try:
                snippet = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            snippet.delete()
            return JsonResponse({"status":200, "msg":"删除成功"})

    if request.method == "PUT":
        print(request.data)
        try:
            snippet = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":200, "msg":"修改成功"})
        return Response({"status":400, "msg":"登录名重复,请检查表单"})


@api_view(["GET","DELETE","POST"])
def admin_group(request):
    '''
    获取组的权限,删除组
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
        queryset = Group.objects.order_by('id').all()[stat:end]
        count = Group.objects.order_by('id').all().count()
        data = {"code": 0, "msg": '', "count": count, "data":[]}


        for databar in queryset:
            perms = Group.objects.get(pk=databar.id).permissions.values('name')
            data_perms = json.dumps(list(perms),ensure_ascii=False)
            data_perms_list = json.loads(data_perms)
            thisid_perm_list = [item[key] for item in data_perms_list for key in item]
            print(thisid_perm_list)

            group_user = Group.objects.get(pk=databar.id).user_set.values('username')
            data_group_user = json.dumps(list(group_user),ensure_ascii=False)
            data_group_user_list = json.loads(data_group_user)
            this_group_user = [item[key] for item in data_group_user_list for key in item]
            print(this_group_user)

            data["data"].append({
                "id": databar.id,
                "name":databar.name,
                "perms":thisid_perm_list,
                "group_user":this_group_user,
            })
        return JsonResponse(data)

    if request.method == "DELETE":
        id =request.POST.get('id')
        try:
            group = Group.objects.get(id=id)
        except Group.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        group.delete()
        return JsonResponse({'status':200,'msg':"删除成功"})

        # ids = request.POST.get('ids')[:-1]
        # id_list = ids.split(', ')
        # for id in id_list:
        #     try:
        #         group = Group.objects.get(id=id)
        #     except Group.DoesNotExist:
        #         return Response(status=status.HTTP_404_NOT_FOUND)
        #     group.delete()
        # return JsonResponse({'status':200,'msg':"删除成功"})

    if request.method == "POST":
        groupname = request.POST.get('groupname')
        Group.objects.create(name=groupname)
        return JsonResponse({'status':200,'msg':"增加成功"})

@api_view(["POST","DELETE"])
def admin_group_user_detail(request):
    '''
    添加，删除组中的用户
    '''
    print(request.data)
    userid = request.POST['userid'].split(', ')
    groupid = request.POST.get('groupid')

    try:
        groupname = Group.objects.get(pk=groupid)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        for id in userid:
            try:
                user = User.objects.get(pk=id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            user.groups.add(groupname)
        return JsonResponse({'status':200,'msg':"添加成功"})

    if request.method == "DELETE":
        for id in userid:
            try:
                user = User.objects.get(pk=id)
            except User.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            user.groups.remove(groupname)
        return JsonResponse({'status':200,'msg':"移除用户"})



@api_view(["PUT","DELETE"])
def admin_group_detail(request):
    '''
    增加，更新，删除组的权限
    '''
    print(request.data)
    #permissions = request.POST['permissions'].split(', ')
    name = request.POST.get('name')
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        permissions = request.POST['permissions'].split(', ')
        group.permissions = permissions
        return JsonResponse({'status':200,'msg':"权限添加成功"})
    if request.method == "DELETE":
        group.permissions.clear()
        return JsonResponse({'status':200,'msg':"权限清空成功"})


@api_view(["POST","DELETE"])
def admin_user_perm_detail(request):
    '''
    添加，删除用户的个人权限
    '''
    print(request.data)
    userid = request.POST.get('userid')
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "POST":
        permission = request.POST['permissions'].split(', ')
        for perm in permission:
            if perm == '':
                return JsonResponse({'status':400,'msg':"请选择权限"})
        user.user_permissions = permission
        return JsonResponse({'status':200,'msg':"添加权限成功"})

    if request.method == "DELETE":
        user.user_permissions.clear()
        return JsonResponse({'status':200,'msg':"权限清空成功"})




