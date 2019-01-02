from django.shortcuts import render
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated




# Create your views here.

# @login_required()
# def admin_list(request):
#     if request.method == "GET":
#         queryset = User.objects.all()
#     return render(request,'Usermanagement/admin_list.html',locals())



@login_required()
def admin_add(request):
    if request.method == "GET":
        pass
        return render(request,'Usermanagement/admin_add.html')



@login_required()
def admin_list(request):
    if request.method == "GET":
        pass
        return render(request,'Usermanagement/admin_list2.html',locals())



@login_required()
def admin_edit(request):
    if request.method == "GET":
        id = request.GET.get('id')
        queryset = User.objects.filter(id=id)
        print(queryset)
        return render(request,'Usermanagement/admin_edit.html',locals())


@login_required()
def admin_role_perm(request):
    if request.method == "GET":
        id = request.GET.get('id')
        user = User.objects.get(id=id)
        perm = user.user_permissions.all()
        #获取该用户拥有的所有权限
        permall = user.get_all_permissions()
        print(permall)

        return render(request, 'Usermanagement/admin_role_perm_edit--测试.html', locals())

@login_required()
def admin_group_list(request):
    if request.method == "GET":
        pass
        return render(request,'Usermanagement/admin_group_list.html',locals())


@login_required()
def admin_group_prem(request):
    if request.method == "GET":
        id = request.GET.get('id')
        groupname = Group.objects.get(id=id)
        premlist = Permission.objects.filter(codename__contains="can")
        return render(request,'Usermanagement/admin_group_perm.html',{"groupname":groupname,"premlist":premlist})

@login_required()
def admin_group_add_user(request):
    if request.method == "GET":
        id = request.GET.get('id')
        groupname = Group.objects.get(pk=id)
        users = User.objects.all()
        group_users = groupname.user_set.all()

        #user = User.objects.get(pk=44)
        #print(user)
        #user.groups.add(groupname)
        #print(user.groups.values('name'))
        return render(request,'Usermanagement/admin_group_add_user.html',{"groupid":id,"groupname":groupname,"users":users,"group_users":group_users})

@login_required()
def admin_role_add_perm(request):
    if request.method == "GET":
        id = request.GET.get('id')
        user = User.objects.get(id=id)
        user_perms = user.user_permissions.values('name')
        user_perms_list = [item[key] for item in user_perms for key in item]
        permlist = Permission.objects.filter()

        return render(request,'Usermanagement/admin_role_add_perm.html',locals())

@login_required()
def admin_group_add(request):
    if request.method == "GET":
        pass
        return render(request,'Usermanagement/admin_group_add.html',locals())