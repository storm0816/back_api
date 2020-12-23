from django.db import models

# Create your models here.


# 分类表
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='分类名')
    sort = models.IntegerField(max_length=10, unique=True, verbose_name='排序')
    remark = models.CharField(max_length=128,  blank=True, null=True, verbose_name='备注')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    lastUpdatedTime = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '分类表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
