from rest_framework_jwt.views import ObtainJSONWebToken, APIView
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from user.serializers import UserSerializer, GroupSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from extend.MyJWTAuthentication import MyTokenViewBase

'''通过 jwt的obtain_jwt_token.as_view()  找到的ObtainJSONWebToken类，进行token登陆
登陆'''


#第一次获取token和令牌
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


#令牌刷新
class MyTokenRefreshView(MyTokenViewBase):
    serializer_class = MyTokenRefreshSerializer


# token验证
class TokenView(APIView):

    def get(self, request, *args, **kwargs):
        res = {'code': 20000, 'message': '获取成功'}
        return JsonResponse(res)


# 用户信息
class UserInfo(APIView):
    def get(self, request, *args, **kwargs, ):
        User = get_user_model()
        if request.method == 'GET':
            print("in get")

            token = request.headers.get('AUTHORIZATION')

            token_msg=authentication.JWTAuthentication().get_validated_token(token)
            print(token_msg)
            user_object=authentication.JWTAuthentication().get_user(token_msg)
            data = {"uid": user_object.id,
                    "name": user_object.username,
                     "first_name": user_object.first_name,
                     "last_name": user_object.last_name,
                     "avatar": user_object.avatar,
                    #  "groups":user_object.groups,
                     "roles": user_object.role,
                     #"introduction": user_object.introduction
            }
            re_data = {"data": data,
                        "code": 20000,
                        "message": "success"
            }
            return JsonResponse(re_data)
