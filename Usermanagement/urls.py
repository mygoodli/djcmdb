from django.conf.urls import url
from . import views

app_name = "Usermanagement"

urlpatterns = [
    url('^admin_list/$',views.admin_list,name='admin_list'),
    url('^admin_add/$',views.admin_add,name='admin_add'),
    url('^admin_edit/$',views.admin_edit,name='admin_edit'),
    url('^admin_edit/(?P<id>[0-9]+)/$',views.admin_edit,name='admin_edit'),
    url('^admin_role_perm/$',views.admin_role_perm,name='admin_role_perm'),
    url('^admin_group_list/$',views.admin_group_list,name="admin_group_list"),
    url('^admin_group_perm/$',views.admin_group_prem,name="admin_group_perm"),
    url('^admin_group_add_user/$',views.admin_group_add_user,name="admin_group_add_user"),
    url('^admin_role_add_perm',views.admin_role_add_perm,name="admin_role_add_perm"),
    url('^admin_group_add/$',views.admin_group_add,name="admin_group_add")

]