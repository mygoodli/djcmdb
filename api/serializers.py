from gamelist.models import *
from rest_framework import serializers
from django.contrib.auth.models import User



class TwzwGamelistSerializer(serializers.ModelSerializer):
    class Meta:
        model =  TwzwGamelist
        fields = ('options','serverid','gamedir','server_port','db_port','serverip','domain_name','gamename','slave_db'
                  ,'message','c_time')

class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')
    date_joined = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M')

    class Meta:
        model = User
        fields = ('id','last_login','is_superuser','username',
                  'first_name','last_name','email','is_active','date_joined')