from rest_framework_jwt.views import APIView
from django.http import JsonResponse

# Create your views here.


class PermissionListView(APIView):

    def get(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        return JsonResponse(re_data)