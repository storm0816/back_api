from rest_framework import permissions
from user.models import UserProfile as User

class MyPermission(permissions.BasePermission):
    """
    自定义权限
    作废作废作废作废作废作废作废作废作废作废作废作废作废作废
    """
    def has_permission(self, request, view):
        try:
            uid = request.user.id
            user_query = User.objects.get(id=uid)
            user_query.has_perm()
        except Exception as ex:
            print('数据库查询失败{0}'.format(ex))
