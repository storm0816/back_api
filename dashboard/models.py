from django.db import models

# Create your models here.

class Dashboard(models.Model):
    name = models.CharField(max_length=16, verbose_name='目录名称', unique=True)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '仪表盘'
        verbose_name_plural = verbose_name
