#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2020/7/15 16:58
# @Author : Yld
# @Site : 
# @File : base.py
# @Software: PyCharm

from functools import wraps


def method_decorator_adaptor(adapt_to, *decorator_args, **decorator_kwargs):
    def decorator_outer(func):
        @wraps(func)
        def decorator(self, *args, **kwargs):
            @adapt_to(*decorator_args, **decorator_kwargs)
            def adaptor(*args, **kwargs):
                return func(self, *args, **kwargs)
            return adaptor(*args, **kwargs)
        return decorator
    return decorator_outer