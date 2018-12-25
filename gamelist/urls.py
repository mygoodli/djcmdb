from django.conf.urls import url
from gamelist import views
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

app_name = 'gamelist'

urlpatterns = [
    url(r'^gamelist/$',views.saltsack_game_list,name="gamelist"),
    url(r'^twzwlist/$',views.twzw_table_list,name="twzwlist"),

    #twzw接收数据接口
    url(r'twzwlist_api/$',views.api_twzwtable,name="api_twzwtable"),
    #twzw url & 接口
    url(r'^re_twzwlist/$',views.table_req_data_api,name="tw_data_api"),
    url(r'^re_twzwlist/(?P<page>[0-9]+)/(?P<limit>[0-9]+)/$', views.table_req_data_api, name='tw_data_api'),

    #bbh url & 接口
    url(r'^bbh_list/$',views.bbh_list,name='bbh_list'),

    url(r'^re_bbhlist/$', views.api_bbh_list_table, name="api_bbh_table"),
    url(r'^re_bbhlist/(?P<page>[0-9]+)/(?P<limit>[0-9]+)/$', views.api_bbh_list_table, name='api_bbh_table'),

]