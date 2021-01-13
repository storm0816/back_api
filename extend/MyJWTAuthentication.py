from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError

from . import Mystatus
from rest_framework_simplejwt.authentication import AUTH_HEADER_TYPES
from rest_framework.response import Response
from rest_framework import generics, status


# 重新自定义返回值
class MyInvalidToken(AuthenticationFailed):
    status_code = Mystatus.HTTP_200_OK
    default_detail = '令牌已过期'
    default_code = '50014'


class MyJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': 'Given a token not valid for any token type',
            'messages': messages,
            'code': 'token_not_valid',
        })


class MyTokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None

    www_authenticate_realm = 'api'

    def get_authenticate_header(self, request):
        return '{0} realm="{1}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            print(e)
            raise MyInvalidToken()

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
