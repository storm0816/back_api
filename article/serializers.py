from rest_framework import serializers
from .models import Category, Label, Article
import json


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'sort', 'remark', 'status', 'createDate', 'updateDate']


'''
自定义返回值
'''
class LabelSerializer(serializers.ModelSerializer):
    categoryName = serializers.SerializerMethodField()

    class Meta:
        model = Label
        fields = ['id', 'name', 'categoryName', 'createDate', 'updateDate']

    def get_categoryName(self, obj):
        """
        获取部门名称
        :param obj: 当前label的实例
        :return: 当前label所在category名称
        参考：https://www.jianshu.com/p/973971880da7
        """
        label = obj
        # print(label.categoryId.name)
        # print(type(label.categoryId.name))
        # categoryName = Category.objects.filter(pk=label.categoryId)[0].name
        return label.categoryId.name


'''
外键反向查询，然后格式化输出
'''


class LabelStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ['id', 'name']


class CategoryLabelListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    labelList = LabelStatusSerializer(many=True, source='label_set')

    class Meta:
        model = Label
        fields = ['id', 'name', 'labelList']


'''文章查询列表'''


class ArticleSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'viewCount', 'thumhup', 'ispublic', 'status', 'updateDate']


'''文章查询列表'''


class ArticleSerializer(serializers.ModelSerializer):
    labelIds = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['id', 'title', 'labelIds', 'imageUrl', 'ispublic', 'summary', 'mdContent', 'htmlContent']

    def get_labelIds(self, obj):
        """
        获取部门名称
        :param obj: 当前label的实例
        :return: 当前label所在category名称
        参考：https://www.jianshu.com/p/973971880da7
        """
        label_list = obj.labelIds
        return json.loads(label_list)



