from rest_framework import serializers
from user.models import Role
from .models import Menu
from django.contrib.auth.models import Permission


# 权限列表
class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Role
        fields = ['id', 'name', 'remark']


# 目录菜单列表
class MenuGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ['id', 'parentId', 'name', 'url', 'code', 'type', 'icon', 'sort', 'createDate', 'updateDate']


class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['id', 'parentId', 'name', 'url', 'code', 'type', 'icon', 'sort', 'createDate', 'updateDate', 'children']

    def get_children(self, obj):
        label = obj
        pk = label.id
        children_query = Menu.objects.filter(parentId=pk)
        if children_query:
            childrenList_ser = MenuSerializer(instance=children_query, many=True)
            return childrenList_ser.data
        else:
            return ''


# 目录菜单列表
class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ['id', 'codename', 'name']

