from django.conf.urls import url
from .views import admin_api

app_name = 'API'

urlpatterns = [
    url('^admin_list_api/$', admin_api.admin_list, name="admin_list_api"),
    url('^admin_detail_api/$', admin_api.admin_detail, name="admin_detail_api")
]