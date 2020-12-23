#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/17 16:44
# @Author : Yld
# @Site : 
# @File : CustomPage.py
# @Software: PyCharm

#rest_framework.pagination不好用，能力不足，还是使用 django的Paginator
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination
from django.core.paginator import Paginator


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2  #指示页面大小的数值
    max_page_size = 5  #表示请求的最大允许页面大小
    # 定制传参
    page_size_query_param = 'pagesize'  #每页显示条数
    page_query_param = 'pagenum'  #当前页码