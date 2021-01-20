from django.db import models

# Create your models here.


# 分类表
class Item(models.Model):
    STATUS_CHOICES = (
        (1, u'正常'),
        (0, u'禁用'),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name='项目名')
    remark = models.CharField(max_length=128,  blank=True, null=True, verbose_name='备注')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=0, verbose_name='状态')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '项目表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 功能表
class Function(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='功能名')
    itemId = models.ForeignKey(to=Item, verbose_name="项目ID", on_delete=models.CASCADE)
    path = models.CharField(max_length=128, blank=True, null=True,verbose_name='程序路劲')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '功能表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 资产表
class Asset(models.Model):
    STATUS_CHOICES = (
        (0, u'已删除'),
        (1, u'待下架'),
        (2, u'正常'),
        (3, u'空闲'),
    )
    #Intranet
    hostname = models.CharField(max_length=128, blank=True, null=True, verbose_name='主机名')
    lanip = models.CharField(max_length=128, unique=True, verbose_name='主机内网IP')
    wanip = models.CharField(max_length=128, blank=True, null=True, verbose_name='主机外网IP')
    functionIds = models.CharField(max_length=128, blank=True, null=True, verbose_name='功能列')
    summary = models.TextField(verbose_name="简介")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="状态")
    itemId = models.ForeignKey(to=Item, verbose_name="项目ID", on_delete=models.SET_NULL, blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '资产表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hostname


# 域名表
class Domain(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='域名')
    itemId = models.ForeignKey(to=Item, verbose_name="项目ID", on_delete=models.CASCADE)
    cname = models.CharField(max_length=128, blank=True, null=True, verbose_name='CNAME')
    elb = models.CharField(max_length=128, blank=True, null=True, verbose_name='负载均衡')
    assetIds = models.CharField(max_length=128, default=[], verbose_name='设备列')
    remark = models.TextField(verbose_name="备注", blank=True, null=True)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '域名表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name