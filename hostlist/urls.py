from django.conf.urls import url
from hostlist import views

app_name = 'hostlist'

urlpatterns = [
    url(r'^hostlist/$', views.hostlist, name='hostlist'),
    url(r'^hostadd/$',views.hostadd,name='hostadd'),
    url(r'^edtil_data/$',views.edit_data,name='edtil_data'),
    url(r'^delete_data/$',views.delete_data,name='delete_data'),
    url(r'^select_data/$',views.select_data,name='select_data'),
    #传导page和limit给view.report GET到数据
    url(r'^report_data/$', views.report_data, name='report_data'),
    url(r'^report_data/(?P<page>[0-9]+)/(?P<limit>[0-9]+)/$', views.report_data, name='report_data'),
]