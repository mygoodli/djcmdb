from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import HostList
from django.db.models import Q

# Create your views here.
#展示页面
@login_required
def hostlist(request):
    pass
    return render(request, 'hostlist/hostlist.html')


#数据编辑
@login_required
def edit_data(request):
    #'''单击一行列表数据进行编辑，从前端传导数据到后端'''
    if request.method == "GET":
        id = request.GET.get('id')
        if id:
            data = HostList.objects.get(id=id)
        else:
            return HttpResponse("id为空")
        return render(request, 'hostlist/hostedit.html', context=locals())
    #提交修改后的数据
    if request.method == "POST":
        id = request.POST.get("id")
        ok = request.POST.get("ok")
        username = request.POST.get("username")
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        city = request.POST.get("city")
        experience = request.POST.get("experience")
        sign = request.POST.get("sign")
        ip = request.POST.get("ip")
        logins = request.POST.get("logins")
        joinTime = request.POST.get("joinTime")

        data={
            'id': id,
            'username': username,
            'email': email,
            'sex': sex,
            'city': city,
            'experience': experience,
            'sign': sign,
            'ip': ip,
            'logins': logins,
            'joinTime': joinTime
              }

        if id == None:
            return HttpResponse("操作无效，id为空值")
        try:
            HostList.objects.filter(id=id).update(**data)

            #修改成功标志
            status = 200
            print(data)
            return JsonResponse({"status":status})
            #return HttpResponse(result)
        except Exception:
            status = 500
            msg = "内部错误"
        #return render(request,'hostlist/hostlist.html',context=locals())
            return JsonResponse({"status": status,"msg":msg})

#增加数据（跳页面方式）
@login_required
def hostadd(request):
    #获取页面
    if request.method == "GET":
        pass
        return render(request, 'hostlist/hostadd.html')
    #提交页面数据
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        sex = request.POST.get("sex")
        city = request.POST.get("city")
        experience = request.POST.get("experience")
        sign = request.POST.get("sign")
        ip = request.POST.get("ip")
        logins = request.POST.get("logins")
        joinTime = request.POST.get("joinTime")

        try:
            host_add = HostList.objects.create(username=username,
                                      email=email,
                                      sex=sex,
                                      city=city,
                                      sign=sign,
                                      experience=experience,
                                      ip=ip,
                                      logins=logins,
                                      joinTime=joinTime)

            host_add.save()
            return JsonResponse({"status":200,"msg":"添加成功"})

        except Exception:
            return JsonResponse({"status":500,"msg":"表单异常，请检查"})

#删除数据
@login_required
@csrf_exempt
def delete_data(request):
    '''批量删除hostlist.html数据'''
    if request.method == "POST":
        ids = request.POST.get('ids')
        print(ids)
        if ids:
            try:
                HostList.objects.extra(where=['id IN ('+ ids[:-1] +')']).delete()
                #返回给前端状态status
                status = 0
            except:
                # 返回给前端状态status
                status = 1
                return JsonResponse({"status":status})
                #return HttpResponse(status,content_type='application/json')

            return JsonResponse({"status": status})
            #return HttpResponse(status,content_type='application/json')

#展示表单
@login_required
def report_data(request):
    '''接受数据库数据接口'''
    if request.method == "GET":
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))

        if page == 1:
            stat = page -1
            end = page * limit
        else:
            stat = (page -1)*limit
            end = page *limit

        queryset = HostList.objects.order_by('-id').all()[stat:end]
        count = HostList.objects.order_by('id').all().count()

        data = {"code":0,"msg":'',"count":count,"data":[]}

        for row in queryset:
            joinTime = row.joinTime.strftime('%Y-%m-%d')
            data["data"].append({
                "id":row.id,
                "username":row.username,
                "email":row.email,
                "sex":row.sex,
                "city":row.city,
                "sign":row.sign,
                "experience":row.experience,
                "ip":row.ip,
                "logins":row.logins,
                "joinTime":joinTime
            })
        return JsonResponse(data)
        #return HttpResponse(json.dumps(data,ensure_ascii=False),content_type="application/json")

#返回搜索的数据表单
@login_required
def select_data(request):
    '''搜索数据返回接口'''
    if request.method == "GET":
        key = request.GET.get('key')
        options = request.GET.get('options')

        if not key:
            data = {
                    "code": 1,   #1为返回msg
                    "msg": '请输入关键字',
                    "count": 1,
                    "data": []
                    }
            return HttpResponse(json.dumps(data, ensure_ascii=False), content_type="application/json")

        #下拉选项为用户名的，get传导&options=user过来
        if options == "user":
            post_list = HostList.objects.filter(Q(username__icontains=key))

            count = post_list.count()

            #print(post_list)
            data = {"code": 0, "msg": '', "count": count, "data": []}
            for post in post_list:
                data["data"].append({
                    "id": post.id,
                    "username": post.username,
                    "email": post.email,
                    "sex": post.sex,
                    "city": post.city,
                    "sign": post.sign,
                    "experience": post.experience,
                    "ip": post.ip,
                    "logins": post.logins,
                    "joinTime": post.joinTime.strftime('%Y-%m-%d')
                })
            return JsonResponse(data)