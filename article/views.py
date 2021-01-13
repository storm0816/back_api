from django.shortcuts import render
from rest_framework_jwt.views import APIView
from django.http import JsonResponse
from extend.MyPageNumber import MyPageNumber
from .models import Category, Label, Article
from .serializers import CategorySerializer, LabelSerializer, CategoryLabelListSerializer, ArticleSearchSerializer, ArticleSerializer
#处理put请求
from django.http import QueryDict
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.


# 查询分类列表
class CategorySearchView(APIView):

    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print(request.data)
        if 'current' in request.data and 'size' in request.data:
            # params修改为可写状态
            request.query_params._mutable = True
            current = request.data['current']
            size = request.data['size']
            print('查询所有数据')
            # 判断前端是否传了搜索字段
            # 前端查询字段为name
            if 'name' in request.data:
                if 'status' in request.data:
                    category_list = Category.objects.filter(name__contains=request.data['name'],
                                                            status=request.data['status']).order_by("id")
                else:
                    category_list = Category.objects.filter(name__contains=request.data['name']).order_by("id")

            else:
                if 'status' in request.data:
                    category_list = Category.objects.filter(status=request.data['status']).order_by("id")
                else:
                    category_list = Category.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = category_list.count()
            page = MyPageNumber()
            page_category = page.paginate_queryset(queryset=category_list, request=request, view=self)
            category_ser = CategorySerializer(instance=page_category, many=True)
            print(category_ser.data)
            re_data['data']['total'] = total
            re_data['data']['records'] = category_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 添加修改分类信息
class CategoryAddUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        if 'sort' in request.data and 'name' in request.data and 'status' in request.data:
            sort = request.data['sort']
            name = request.data['name']
            status = request.data['status']
            remark = request.data['remark']
            try:
                sql = Category.objects.create(name=name, status=status, sort=sort, remark=remark)
                sql.save()
            except Exception as ex:
                msg = "添加失败: {ex}".format(ex=ex)
                re_data['code'] = 40000
                re_data['message'] = msg
        else:
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def put(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "更新成功"
        put = QueryDict(request.body)
        put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        put_dict = eval(put_str)  # 将str类型转换为字典类型
        if 'sort' in request.data and 'name' in request.data and 'status' in request.data and 'id' in request.data:
            id = put_dict.get("id")  # 获取传递参数
            print('更新ID：', id)
            sort = put_dict.get("sort")
            name = put_dict.get("name")
            status = put_dict.get("status")
            remark = put_dict.get("remark")
            # 更新数据
            try:
                Category.objects.filter(pk=id).update(name=name, status=status, sort=sort, remark=remark)
            except Exception as ex:
                msg = "更新失败: {ex}".format(ex=ex)
                re_data['code'] = 40000
            re_data['message'] = msg
            return JsonResponse(re_data, safe=False)
        else:
            msg = '更新失败，参数异常'
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询分类信息
class CategoryGetDelView(APIView):
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询ID：', id)
        try:
            category_list = Category.objects.filter(pk=id).first()
            category_ser = CategorySerializer(category_list)
            re_data['data'] = category_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def delete(self, request, id,  *args, **kwargs,):
        print('删除:', id)
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:
            Category.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


#查询标签列表
class LabelSearchView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print(request.data)
        if 'current' in request.data and 'size' in request.data:
            # params修改为可写状态
            request.query_params._mutable = True
            current = request.data['current']
            size = request.data['size']
            print('查询所有数据')
            # 判断前端是否传了搜索字段
            # 前端查询字段为name
            if 'name' in request.data:
                if 'categoryName' in request.data:
                    lable_list = Label.objects.filter(name__contains=request.data['name'],
                                                            categoryId=request.data['categoryId']).order_by("id")
                else:
                    lable_list = Label.objects.filter(name__contains=request.data['name']).order_by("id")

            else:
                if 'categoryId' in request.data:
                    lable_list = Label.objects.filter(categoryId=request.data['categoryId']).order_by("id")
                else:
                    lable_list = Label.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = lable_list.count()
            page = MyPageNumber()
            page_Lable = page.paginate_queryset(queryset=lable_list, request=request, view=self)
            lable_ser = LabelSerializer(instance=page_Lable, many=True)
            re_data['data']['total'] = total
            re_data['data']['records'] = lable_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 查询所有正常状态的分类
class CategoryListView(APIView):
    def get(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        try:
            category_list = Category.objects.all().order_by("id")
            category_ser = CategorySerializer(instance=category_list, many=True)
            re_data['data'] = category_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 添加修改标签信息
class LabelAddUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        if 'name' in request.data and 'categoryId' in request.data:
            print('添加标签', id)
            categoryId = request.data['categoryId']
            name = request.data['name']
            try:
                category = Category.objects.filter(pk=categoryId).first()
                sql = Label.objects.create(name=name, categoryId=category)
                sql.save()
            except Exception as ex:
                msg = "添加失败: {ex}".format(ex=ex)
                print(msg)
                re_data['code'] = 40000
                re_data['message'] = msg
        else:
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def put(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "更新成功"
        # put = QueryDict(request.body)
        # put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        # put_dict = eval(put_str)  # 将str类型转换为字典类型
        if 'name' in request.data and 'categoryId' in request.data:
            print('更新标签：',id)
            id = request.data['id'] # 获取传递参数
            name = request.data['name']
            categoryId = request.data['categoryId']
            # 更新数据
            try:
                category = Category.objects.filter(pk=categoryId).first()
                Label.objects.filter(pk=id).update(name=name, categoryId=category)
            except Exception as ex:
                msg = "更新失败: {ex}".format(ex=ex)
                re_data['code'] = 40000
            re_data['message'] = msg
            return JsonResponse(re_data, safe=False)
        else:
            msg = '更新失败，参数异常'
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询删除标签信息
class LabelGetDelView(APIView):
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询标签ID：', id)
        try:
            label_list = Label.objects.filter(pk=id).first()
            label_ser = LabelSerializer(label_list)
            re_data['data'] = label_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def delete(self, request, id,  *args, **kwargs,):
        print('标签删除:', id)
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:

            Label.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询所有正常分类和标签
class CategoryLabelListView(APIView):
    def get(self, request,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('正常分类和标签')
        try:
            category_list = Category.objects.all()
            category_ser = CategoryLabelListSerializer(category_list, many=True)
            re_data['data'] = category_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


#查询文章列表
class ArticleSearchView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print(request.data)
        if 'current' in request.data and 'size' in request.data:
            # params修改为可写状态
            request.query_params._mutable = True
            current = request.data['current']
            size = request.data['size']
            print('查询所有数据')
            # 判断前端是否传了搜索字段
            # 前端查询字段为name
            if 'title' in request.data:
                if 'status' in request.data:
                    article_list = Article.objects.filter(title__contains=request.data['title'],
                                                            status=request.data['status']).order_by("id")
                else:
                    article_list = Article.objects.filter(title__contains=request.data['title']).order_by("id")

            else:
                if 'status' in request.data:
                    article_list = Article.objects.filter(status=request.data['status']).order_by("id")
                else:
                    article_list = Article.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = article_list.count()
            page = MyPageNumber()
            page_Lable = page.paginate_queryset(queryset=article_list, request=request, view=self)
            article_ser = ArticleSearchSerializer(instance=page_Lable, many=True)
            re_data['data']['total'] = total
            re_data['data']['records'] = article_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 查询删除文章信息
class ArticleDetailView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询文章ID：', id)
        try:
            article_list = Article.objects.filter(pk=id).first()
            article_ser = ArticleSerializer(article_list)
            print(article_ser.data)
            re_data['data'] = article_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def delete(self, request, id,  *args, **kwargs,):
        print('标签删除:', id)
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:

            Label.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)



