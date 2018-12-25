"""mycmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from login import views
from django.conf.urls import include
from .view import obtain_expiring_auth_token
from rest_framework_jwt.views import obtain_jwt_token,verify_jwt_token

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index,name='index'),
    url(r'error',views.error_show,name='error'),
    #url(r'^api/token/', obtain_expiring_auth_token, name='api-token'),
    url(r'^api-token-auth/', obtain_jwt_token,name="api-token-auth"),
    url(r'^api-token-verify/', verify_jwt_token),

    url(r'^',include('api.urls')),
    url(r'^',include('login.urls')),
    url(r'^',include('captcha.urls')),
    url(r'^',include('hostlist.urls')),
    url(r'^',include('gamelist.urls')),
    url(r'^',include('Usermanagement.urls'))
]
