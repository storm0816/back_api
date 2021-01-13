from django.db import models
from django.contrib.auth.models import Permission

# Create your models here.


class Menu(models.Model):
    TYPE_CHOICES = (
        (1, u'目录'),
        (2, u'菜单'),
        (3, u'按钮'),
    )
    parentId = models.IntegerField(verbose_name='父目录', blank=True, null=True)
    name = models.CharField(max_length=16, verbose_name='目录名称', unique=True)
    url = models.CharField(max_length=16, verbose_name='路径', blank=True, null=True)
    code = models.CharField(max_length=16, verbose_name='权限标识', blank=True, null=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=0, verbose_name='类型')
    icon = models.CharField(max_length=64, verbose_name='图标', blank=True, null=True)
    sort = models.IntegerField(verbose_name='排序', blank=True, null=True)
    remark = models.TextField(verbose_name='备注', blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # 权限ID 与 Permission表关联
    permissionId = models.IntegerField(verbose_name='父目录', blank=True, null=True)

    class Meta:
        verbose_name = '菜单表'
        verbose_name_plural = verbose_name
