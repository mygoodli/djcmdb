from django.conf.urls import url
from . import views

app_name = "Usermanagement"

urlpatterns = [
    url('^admin_list/$',views.admin_list,name='admin_list'),
    url('^admin_add/$',views.admin_add,name='admin_add'),
    url('^admin_edit/$',views.admin_edit,name='admin_edit'),
    url('^admin_edit/(?P<id>[0-9]+)/$',views.admin_edit,name='admin_edit'),
    url('^admin_role_list/$',views.admin_role_list,name='admin_role_list')
]