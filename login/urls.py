from django.conf.urls import url
from login import views



urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/',views.logout_out,name='logout'),
    url(r'^welcome/', views.welcome, name='welcome'),
    ]