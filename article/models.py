from django.db import models

# Create your models here.


# 分类表
class Category(models.Model):
    STATUS_CHOICES = (
        (1, u'正常'),
        (0, u'禁用'),
    )
    name = models.CharField(max_length=128, unique=True, verbose_name='分类名')
    sort = models.IntegerField(unique=True, verbose_name='排序')
    remark = models.CharField(max_length=128,  blank=True, null=True, verbose_name='备注')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=0, verbose_name='状态')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '分类表'
        verbose_name_plural = verbose_name

        permissions = (
            ('view_customer_list',u"查看客户列表"),  # 权限字段名称及其解释
            ('view_customer_info',u"查看客户详情"),
            ('edit_own_customer_info',u"修改客户信息"),
        )

    def __str__(self):
        return self.name




# 标签表
class Label(models.Model):
    name = models.CharField(max_length=128, unique=True, verbose_name='标签名')
    categoryId = models.ForeignKey(to=Category, verbose_name="分类ID", on_delete=models.CASCADE)
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '标签表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章表
class Article(models.Model):
    STATUS_CHOICES = (
        (0, u'已删除'),
        (1, u'未审核'),
        (2, u'审核通过'),
        (3, u'审核未通过'),
    )
    ISPUBLIC_CHOICES = (
        (1, u'公开'),
        (0, u'不公开'),
    )
    title = models.CharField(max_length=128, unique=True, verbose_name='标签名')
    viewCount = models.CharField(max_length=128, default=0, verbose_name='浏览数')
    thumhup = models.CharField(max_length=128, default=0, verbose_name='点赞数')
    labelIds = models.CharField(max_length=128, verbose_name='标签列')
    summary = models.CharField(max_length=256, verbose_name="简介")
    imageUrl = models.CharField(max_length=256, verbose_name="图片链接")
    mdContent = models.CharField(max_length=256, verbose_name="富文本")
    htmlContent = models.CharField(max_length=256, verbose_name="html富文本")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name="审核状态")
    ispublic = models.IntegerField(choices=ISPUBLIC_CHOICES, default=0, verbose_name="是否公开")
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updateDate = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')

    class Meta:
        verbose_name = '文章表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
