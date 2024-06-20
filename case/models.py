from django.db import models

# Create your models here.
"""
分组表：
分组id，分组code，分组名称，直属领导

用户表:
用户id,用户编号,用户名,密码,昵称,部门,身份（超级管理员、管理员、部门领导、组长、普通用户）,创建时间,更新时间,是否删除

版本表：
版本id，版本号，版本名称，所属分组，
"""
class Grouping(models.Model):
    group_code = models.CharField(verbose_name='分组编号',max_length=64)
    group_name = models.CharField(verbose_name='分组名称',max_length=64)
    leader_name = models.CharField(verbose_name='组长姓名',max_length=64)
    desc = models.CharField(verbose_name='更多信息',max_length=128,blank=True)
    create_time = models.DateTimeField(verbose_name='创建时间')

class User(models.Model):
    user_code = models.CharField(verbose_name='用户编号',max_length=64, unique=True)
    user_name = models.CharField(verbose_name='用户名',max_length=64, unique=True)
    password = models.CharField(verbose_name='密码',max_length=64, unique=False)
    nickname = models.CharField(verbose_name='用户昵称',max_length=64, unique=False)
    user_head = models.FileField(verbose_name='用户头像')
    group = models.ForeignKey(verbose_name='所属分组',to=Grouping, on_delete=models.CASCADE)
    role_choices = ((1,"普通用户"),(2,"组长"),(3,"部门主管"),(4,"管理员"),(5,"超级管理员"))
    role =models.SmallIntegerField(verbose_name='角色身份',choices=role_choices,default=1)
    create_time = models.DateTimeField(verbose_name='创建时间')


class Version(models.Model):
    version_name = models.CharField(verbose_name='版本名称',max_length=64)
    desc = models.TextField(verbose_name='版本描述',max_length=128)
    create_time = models.DateTimeField(verbose_name='创建时间')


