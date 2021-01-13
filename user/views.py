from rest_framework_jwt.views import ObtainJSONWebToken, APIView
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from user.serializers import UserSerializer, GroupSerializer, MyTokenObtainPairSerializer, MyTokenRefreshSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from extend.MyJWTAuthentication import MyTokenViewBase
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        print('authenticators:', request.authenticators)
        print('successful_authenticator:', request.successful_authenticator)
        print('authenticate: ', request.successful_authenticator.authenticate(request))
        print('authenticate_header: ', request.successful_authenticator.authenticate_header(request))
        print('get_header: ', request.successful_authenticator.get_header(request))
        print('get_raw_token: ', request.successful_authenticator.get_raw_token(request.successful_authenticator.get_header(request)))
        print('get_validated_token: ', request.successful_authenticator.get_validated_token(request.successful_authenticator.get_raw_token(request.successful_authenticator.get_header(request))))
        print('get_user: ', request.successful_authenticator.get_user(request.successful_authenticator.get_validated_token(request.successful_authenticator.get_raw_token(request.successful_authenticator.get_header(request)))))
        print('www_authenticate_realm: ', request.successful_authenticator.www_authenticate_realm)
        return Response("OK")
