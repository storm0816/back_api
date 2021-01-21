from rest_framework import serializers
from .models import Item, Function, Asset, Domain
import json


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'owner', 'remark', 'status', 'createDate', 'updateDate']


'''
自定义返回值
'''
class FunctionSerializer(serializers.ModelSerializer):
    itemName = serializers.SerializerMethodField()

    class Meta:
        model = Function
        fields = ['id', 'name', 'path', 'itemName', 'createDate', 'updateDate']

    def get_itemName(self, obj):
        """
        获取部门名称
        :param obj: 当前label的实例
        :return: 当前label所在category名称
        参考：https://www.jianshu.com/p/973971880da7
        """
        function = obj
        # print(label.categoryId.name)
        # print(type(label.categoryId.name))
        # categoryName = Category.objects.filter(pk=label.categoryId)[0].name
        return function.itemId.name


'''
外键反向查询，然后格式化输出
'''


class FunctionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Function
        fields = ['id', 'name', 'path']


class ItemFunctionListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    functionList = FunctionStatusSerializer(many=True, source='function_set')

    class Meta:
        model = Function
        fields = ['id', 'name', 'functionList']


class AssetSerializer(serializers.ModelSerializer):
    functionIds = serializers.SerializerMethodField()

    class Meta:
        model = Asset
        fields = ['id', 'hostname', 'lanip', 'wanip', 'functionIds', 'summary', 'status', 'itemId', 'updateDate']

    def get_functionIds(self, obj):
        """
        获取部门名称
        :param obj: 当前label的实例
        :return: 当前label所在category名称
        参考：https://www.jianshu.com/p/973971880da7
        """
        function_list = obj.functionIds
        return json.loads(function_list)

#
# class AssetStatusSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Asset
#         fields = ['id', 'name']
#
#     def get_name(self, obj):
#         return obj.lanip
#
#
# class ItemAssetListSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     name = serializers.CharField()
#     assetList = AssetStatusSerializer(many=True, source='asset_set')
#
#     class Meta:
#         model = Asset
#         fields = ['id', 'name', 'assetList']
#

class DomainSerializer(serializers.ModelSerializer):
    assetIds = serializers.SerializerMethodField()
    itemName = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = ['id', 'name', 'itemId', 'itemName', 'cname', 'elb', 'assetIds', 'remark']

    def get_assetIds(self, obj):
        # assetIds 列表形式返回
        asset_list = obj.assetIds
        return json.loads(asset_list)

    def get_itemName(self, obj):
        # 通过itemId  查询item中的name
        domain = obj
        return domain.itemId.name