from functools import wraps
from jsonpath import jsonpath
import json


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


def find(target, dictData, notFound=0):
    # ordereddict 有序字典
    queue = dictData
    for i in range(len(queue)):
        data = queue[i]
        code_list = jsonpath(data, '$..code')
        if target in code_list:
            return data
    return notFound


def abridge(dictData):
    queue = dictData
    for data in queue['children']:
        # 清空二级目录下的按钮信息
        if len(data['children']) > 0:
            data['children'] = ''
        # 清空一级目录下的按钮信息
        if data['type'] == 3:
            queue['children'] = ''
    return queue
