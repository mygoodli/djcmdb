from django.shortcuts import render
from gamelist.API.salt_api import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TwzwGamelist
from .models import BbhGamelist
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import permission_required


# Create your views here.

#输入命令，返回结果
@permission_required('gamelist.can_read_BbhGamelist',login_url="error.html")
@login_required()
@csrf_exempt
def saltsack_game_list(request):
    '''
    :param request:接受前端输入的主机Ip和命令shell
    :return: 返回结果给前端
    '''
    if request.method == "POST":
        key = request.POST.get('key')
        cmd = request.POST.get('cmd')

        try:
            sa = SaltApi()
            resutl = sa.host_remote_execution_module(key, 'cmd.run', cmd)
            return JsonResponse(resutl,safe=False)
        except:
            resutl = {key: "异常!!!"}
            return JsonResponse(resutl,safe=False)

    else:
        return render(request, 'gamelist/gamelist.html')

#展示页面
@permission_required('gamelist.can_read_TwzwGamelist',login_url="error.html")
@login_required()
def twzw_table_list(request):
    '''展示页面'''
    return render(request, 'gamelist/twzw_list.html', locals())


#表单返回
@api_view(['POST','GET'])
@permission_classes((IsAuthenticated,))
def table_req_data_api(request):
    '''数据库数据接口
        GET为返回前端列表接口
        POST收集外部信息，存进数据库接口
    '''
    if request.method == "GET":
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))
        # 搜索，前端传导的数据
        key = request.GET.get('key')

        if page == 1:
            stat = page - 1
            end = page * limit
        else:
            stat = (page - 1) * limit
            end = page * limit

            # conditions and options 存在返回真
        if key:
            #查询游戏服ID
            try:
                options_list = TwzwGamelist.objects.filter(serverid=key)[stat:end]
                count = TwzwGamelist.objects.filter(serverid=key).all().count()
                #layui表单API需要接受后端的数据样式
                data = {"code": 0,
                        "msg": '',
                        "count": count,
                        "data": []
                        }
                for row in options_list:
                     data["data"].append({
                        "id": row.id,
                        "options": row.options,
                        "serverid": row.serverid,
                        "gamedir": row.gamedir,
                        "db_port": row.db_port,
                        "serverip": row.serverip,
                        "domain_name": row.domain_name,
                        "gamename": row.gamename,
                        "subordinate_db": row.subordinate_db,
                        "message": row.message
                    })
                return JsonResponse(data)

            except:
                options_list = TwzwGamelist.objects.filter(gamename__contains=key)[stat:end]
                count = TwzwGamelist.objects.filter(gamename__contains=key).all().count()
                # layui表单API需要接受后端的数据样式
                data = {"code": 0,
                        "msg": '',
                        "count": count,
                        "data": []
                        }
                for row in options_list:
                    data["data"].append({
                        "id": row.id,
                        "options": row.options,
                        "serverid": row.serverid,
                        "gamedir": row.gamedir,
                        "server_port": row.server_port,
                        "db_port": row.db_port,
                        "serverip": row.serverip,
                        "domain_name": row.domain_name,
                        "gamename": row.gamename,
                        "subordinate_db": row.subordinate_db,
                        "message": row.message
                        })
                return JsonResponse(data)

        else:
            # 直接展示表单
            queryset = TwzwGamelist.objects.order_by('serverid').all()[stat:end]
            count = TwzwGamelist.objects.order_by('serverid').all().count()

            data = {"code": 0, "msg": '', "count": count, "data": []}

            for row in queryset:
                data["data"].append({
                    "id": row.id,
                    "options": row.options,
                    "serverid": row.serverid,
                    "gamedir": row.gamedir,
                    "server_port": row.server_port,
                    "db_port": row.db_port,
                    "serverip": row.serverip,
                    "domain_name": row.domain_name,
                    "gamename": row.gamename,
                    "subordinate_db": row.subordinate_db,
                    "message": row.message
                })
            return JsonResponse(data)

#收集数据接口
@api_view(['POST'])
@permission_classes((IsAuthenticated,))

@csrf_exempt
@login_required()
def api_twzwtable(request):
    if request.method == "POST":
        # print(request.user, request.user.id)
        # return HttpResponse("Welcome.")
        options = request.POST.get('options')
        serverid = request.POST.get('serverid')
        gamedir = request.POST.get('gamedir')
        server_port = request.POST.get('server_port')
        db_port = request.POST.get('db_port')
        serverip = request.POST.get('serverip')
        domain_name = request.POST.get('domain_name')
        gamename = request.POST.get('gamename')
        subordinate_db = request.POST.get('subordinate_db')
        message = request.POST.get('message')

        try:
            TwzwGamelist.objects.get_or_create(
                options=options,
                serverid=serverid,
                gamedir=gamedir,
                server_port=server_port,
                db_port=db_port,
                serverip=serverip,
                domain_name=domain_name,
                gamename=gamename,
                subordinate_db=subordinate_db,
                message=message
            )
            return HttpResponse('添加成功')
        except Exception as e:
            print(serverid+'失败')
            return HttpResponse(e)

#######################################################################################################################
#bbh_list

@login_required()
@permission_required('gamelist.can_read_BbhGamelist',login_url="error.html")
def bbh_list(request):

    return render(request, 'gamelist/bbh_list.html')


@login_required()
def api_bbh_list_table(request):
    if request.method == "GET":
        page = int(request.GET.get('page'))
        limit = int(request.GET.get('limit'))

        print(page)

        if page == 1:
            stat = page - 1
            end = page * limit
        else:
            stat = (page - 1) * limit
            end = page * limit

        #展示数据
        bbh_queryset = BbhGamelist.objects.order_by('server_id').all()[stat:end]
        count = BbhGamelist.objects.order_by('server_id').all().count()

        data = {"code": 0,
                "msg": '',
                "count": count,
                "data": []
                }
        for bbh in bbh_queryset:
            data["data"].append({
                "options": bbh.options,
                "mongo_ip": bbh.mongo_ip,
                "mysql_ip": bbh.mysql_ip,
                "gameserver_dir": bbh.gameserver_dir,
                "gameserver_ip": bbh.gameserver_ip,
                "gameserver_port": bbh.gameserver_port,
                "grand_port": bbh.grand_port,
                "server_id": bbh.server_id,
                "mysqldb_name": bbh.mysqldb_name,
                "domain_name": bbh.domain_name,
                "gameserver_name":bbh.gameserver_name,
                "note": bbh.note,
                })
        return JsonResponse(data)