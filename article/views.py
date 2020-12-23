from django.shortcuts import render
from rest_framework_jwt.views import APIView
from django.http import JsonResponse

# Create your views here.


# 查询分类列表
class CategorySearchView(APIView):
    def post(self, request, *args, **kwargs):

        return JsonResponse('haha')
