from django.db import models

# Create your models here.

class TwzwGamelist(models.Model):
    '''游戏服列表'''
    options = models.CharField(max_length=64,verbose_name="合服状态")
    serverid = models.IntegerField(verbose_name="游戏服id")
    gamedir = models.CharField(max_length=128,verbose_name="游戏目录")
    server_port = models.IntegerField(verbose_name="游戏服端口")
    db_port = models.IntegerField(verbose_name="游戏服数据库端口")
    serverip = models.CharField(max_length=128,verbose_name="游戏服ip")
    domain_name = models.CharField(max_length=256,verbose_name="域名")
    gamename = models.CharField(max_length=256,verbose_name="游戏服名字")
    slave_db = models.CharField(max_length=256,verbose_name="游戏服从库ip")
    message = models.CharField(max_length=256,verbose_name="附加信息")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.gamename

    class Meta:
        verbose_name="游戏服名字"
        verbose_name_plural="游戏服名字"
        db_table="twzwgamelist"

        permissions = (
            ("can_read_TwzwGamelist", "读取塔王之王权限"),
            ("can_change_TwzwGamelist", "更改塔王之王权限"),
            ("can_add_TwzwGamelist", "添加塔王之王权限"),
            ("can_delete_TwzwGamelist", "删除塔王之王权限"),
        )


class BbhGamelist(models.Model):
    '''爆兵英雄游戏服列表'''
    gender = (
        ('yes_options', '#已合服'),
        ('no_options', 'gatfile')
    )

    options = models.CharField(max_length=128,choices=gender,verbose_name="合服状态")
    mongo_ip = models.CharField(max_length=128,verbose_name="mongodb地址")
    mysql_ip = models.CharField(max_length=128,verbose_name="mysql地址")
    gameserver_dir = models.CharField(max_length=256,verbose_name="游戏服目录")
    gameserver_ip = models.CharField(max_length=128,verbose_name="游戏服ip地址")
    gameserver_port = models.IntegerField(verbose_name="游戏端口")
    grand_port = models.IntegerField(verbose_name="战报端口")
    server_id = models.IntegerField(primary_key=True,verbose_name="游戏服serverid")
    mysqldb_name = models.CharField(max_length=256,verbose_name="mysqlDBName")
    domain_name = models.CharField(max_length=256,verbose_name="域名")
    gameserver_name = models.CharField(max_length=256,verbose_name="游戏服名字")
    note = models.CharField(max_length=256,verbose_name="备注")

    def __str__(self):
        return self.gameserver_name

    class Meta:
        verbose_name = "bbh5爆兵英雄"
        verbose_name_plural = "bbh5爆兵英雄"
        db_table = "bbhgamelist"

        permissions = (
            ("can_read_BbhGamelist", "读取爆兵英雄权限"),
            ("can_change_BbhGamelist", "更改爆兵英雄权限"),
            ("can_add_BbhGamelist", "添加爆兵英雄权限"),
            ("can_delete_BbhGamelist", "删除爆兵英雄权限"),
        )