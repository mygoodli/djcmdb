from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from api import serializers



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
def admin_role_list(request):
    if request.method == "GET":
        pass
        return render(request,'Usermanagement/admin_role_list.html',locals())
