from django.shortcuts import render
from rest_framework_jwt.views import APIView
from django.http import JsonResponse

from extend.data import *

# Create your views here.


class MenuUserList(APIView):
    permission_classes = []

    def get(self, request, userid, *args, **kwargs):
        print(userid)
        res = {'code': 20000, 'message': '获取成功'}
        data = MenUserList()
        res['data'] = data
        return JsonResponse(res)
