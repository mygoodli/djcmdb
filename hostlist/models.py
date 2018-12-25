from django.db import models

# Create your models here.
class HostList(models.Model):
    '''测试列表'''

    gender = (
        ('male','男'),
        ('female','女')
    )

    username = models.CharField(max_length=64,verbose_name='用户名')
    email = models.EmailField(verbose_name='邮件地址')
    sex = models.CharField(max_length=32,choices=gender,verbose_name='性别')
    city = models.CharField(max_length=64,verbose_name='城市')
    sign = models.CharField(max_length=128,verbose_name='签名')
    experience = models.IntegerField(verbose_name='积分')
    ip = models.CharField(max_length=128,verbose_name='IP')
    logins = models.IntegerField(verbose_name='登录次数')
    joinTime = models.DateField(verbose_name='加入时间')
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["-c_time"]