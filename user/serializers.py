from django.contrib.auth.models import Group
from user.models import UserProfile as User
from user.models import Role
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings


class UserSerializer(serializers.ModelSerializer):
    nickName = serializers.CharField(source='nickname')
    isAccountNonExpired = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'nickName', 'mobile', 'email', 'isAccountNonExpired']

    def get_isAccountNonExpired(self, obj):
        label = obj
        if label.is_active:
            return 1
        else:
            return 0



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print('in MyTokenObtainPairSerializer')
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        token['code'] = 20000
        return token
    def validate(self,attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        userInfo = dict()
        userInfo['uid'] = self.user.id
        userInfo['name'] = self.user.username
        userInfo['first_name'] = self.user.first_name
        userInfo['last_name'] = self.user.last_name
        userInfo['avatar'] = self.user.avatar
        userInfo['roles'] = self.user.role
        userInfo['mobile'] = self.user.mobile
        data['userInfo'] = userInfo
        re_data = dict()
        re_data['code'] = 20000
        re_data['message'] = 'success'
        re_data['data'] = data
        return re_data


class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = RefreshToken(attrs['refresh'])
        re_data = dict()
        data = {'access': str(refresh.access_token)}
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass
            refresh.set_jti()
            refresh.set_exp()
            data['refresh'] = str(refresh)
        #自定义返回值
        re_data['code'] = 20000
        re_data['message'] = 'success'
        re_data['data'] = data
        return re_data


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name', 'remark']


