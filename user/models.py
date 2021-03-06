from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
import time
from django.utils import timezone

# Create your models here.


class UserProfile(AbstractUser):
    avatar = models.CharField(max_length=128, verbose_name='用户头像', blank=True, null=True)
    nickname = models.CharField(max_length=32, verbose_name='用户昵称', blank=True, null=True)
    role = models.CharField(max_length=16, verbose_name='角色', blank=True, null=True)
    mobile = models.IntegerField(verbose_name='手机号码', blank=True, null=True)

    class Meta:
        verbose_name = '用户信息表'
        verbose_name_plural = verbose_name


class Role(Group):
    remark = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '角色表'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.name



