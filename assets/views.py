from django.shortcuts import render
from rest_framework_jwt.views import APIView
from django.http import JsonResponse
from extend.MyPageNumber import MyPageNumber
from .models import Item, Function, Asset, Domain
from .serializers import ItemSerializer, FunctionSerializer, ItemFunctionListSerializer, AssetSerializer, \
    DomainSerializer
from datetime import datetime
import re
#处理put请求
from django.http import QueryDict
# Create your views here.


# 查询项目列表
class ItemSearchView(APIView):

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
                    item_list = Item.objects.filter(name__icontains=request.data['name'],
                                                            status=request.data['status']).order_by("id")
                else:
                    item_list = Item.objects.filter(name__icontains=request.data['name']).order_by("id")

            else:
                if 'status' in request.data:
                    item_list = Item.objects.filter(status=request.data['status']).order_by("id")
                else:
                    item_list = Item.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = item_list.count()
            page = MyPageNumber()
            page_category = page.paginate_queryset(queryset=item_list, request=request, view=self)
            category_ser = ItemSerializer(instance=page_category, many=True)
            print(category_ser.data)
            re_data['data']['total'] = total
            re_data['data']['records'] = category_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 添加修改项目信息
class ItemAddUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        if 'name' in request.data and 'status' in request.data:
            name = request.data.get('name', None)
            status = request.data.get('status', None)
            remark = request.data.get('remark', None)
            try:
                sql = Item.objects.create(name=name, status=status, remark=remark)
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
        if 'name' in request.data and 'status' in request.data and 'id' in request.data:
            id = put_dict.get("id")  # 获取传递参数
            print('更新ID：', id)
            name = put_dict.get("name", None)
            status = put_dict.get("status", None)
            remark = put_dict.get("remark", None)
            # 更新数据
            try:
                Item.objects.filter(pk=id).update(name=name, status=status, remark=remark, updateDate=datetime.now())
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


# 查询删除项目信息
class ItemGetDelView(APIView):
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询ID：', id)
        try:
            item_list = Item.objects.filter(pk=id).first()
            item_list_ser = ItemSerializer(item_list)
            re_data['data'] = item_list_ser.data
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
            Item.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询所有正常状态的项目
class ItemListView(APIView):
    def get(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        try:
            item_list = Item.objects.filter(status=1).order_by("id")
            item_ser = ItemSerializer(instance=item_list, many=True)
            re_data['data'] = item_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


#查询功能列表
class FunctionSearchView(APIView):
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
            name = request.data.get('name', None)
            itemId = request.data.get('itemId', None)
            if name:
                if itemId:
                    function_list = Function.objects.filter(name__contains=request.data['name'],
                                                            itemId=request.data['itemId']).order_by("id")
                else:
                    function_list = Function.objects.filter(name__contains=request.data['name']).order_by("id")

            else:
                if itemId:
                    function_list = Function.objects.filter(itemId=request.data['itemId']).order_by("id")
                else:
                    function_list = Function.objects.all().order_by("id")

            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = function_list.count()
            page = MyPageNumber()
            page_Lable = page.paginate_queryset(queryset=function_list, request=request, view=self)
            function_ser = FunctionSerializer(instance=page_Lable, many=True)
            re_data['data']['total'] = total
            re_data['data']['records'] = function_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 添加修改标签信息
class FunctionAddUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        if 'name' in request.data and 'itemId' in request.data:
            print('添加功能', id)
            name = request.data.get('name', None)
            itemId = request.data.get('itemId', None)
            path = request.data.get('path', None)
            try:
                item = Item.objects.filter(pk=itemId).first()
                sql = Function.objects.create(name=name, itemId=item, path=path)
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
        if 'name' in request.data and 'itemId' in request.data:
            id = request.data['id'] # 获取传递参数
            name = request.data['name']
            itemId = request.data['itemId']
            path = request.data.get('path', None)
            # 更新数据
            try:
                item = Item.objects.filter(pk=itemId).first()
                Function.objects.filter(pk=id).update(name=name, itemId=item, path=path, updateDate=datetime.now())
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


# 查询删除功能信息
class FunctionGetDelView(APIView):
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询标签ID：', id)
        try:
            function_list = Function.objects.filter(pk=id).first()
            function_ser = FunctionSerializer(function_list)
            re_data['data'] = function_ser.data
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

            Function.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询所有正常项目和功能
class ItemFunctionListView(APIView):
    def get(self, request,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('正常分类和标签')
        try:
            item_list = Item.objects.all()
            item_ser = ItemFunctionListSerializer(item_list, many=True)
            re_data['data'] = item_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询所有正常项目和功能
class ItemAssetListView(APIView):
    def get(self, request, itemid, *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('正常分类和标签')
        try:
            asset_query = Asset.objects.filter(itemId=itemid).order_by("id")
            asset_ser = AssetSerializer(asset_query, many=True)
            re_data['data'] = asset_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询设备列表
class AssetSearchView(APIView):

    def post(self, request,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        '''
        { code: 1, name: '设备名称' },
        { code: 2, name: '内网IP' },
        { code: 3, name: '外网IP' },
        '''
        query_select = {1: 'hostname__contains', 2: 'lanip__contains', 3: 'wanip__contains'}
        print(request.data)
        if 'current' in request.data and 'size' in request.data:
            # params修改为可写状态
            request.query_params._mutable = True
            current = request.data['current']
            size = request.data['size']
            select = request.data.get('select', None)
            name = request.data.get('name', None)
            itemId = request.data.get('itemId', None)
            status = request.data.get('status', None)
            search_dict = dict()
            if select:
                search_dict[query_select[select]] = name
            if itemId:
                search_dict['itemId'] = itemId
            if status:
                search_dict['status'] = status
            if select or itemId or status:
                asset_query = Asset.objects.filter(**search_dict).order_by("id")
            else:
                asset_query = Asset.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = asset_query.count()
            page = MyPageNumber()
            page_Lable = page.paginate_queryset(queryset=asset_query, request=request, view=self)
            asset_ser = AssetSerializer(instance=page_Lable, many=True)
            re_data['data']['total'] = total
            re_data['data']['records'] = asset_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'
        return JsonResponse(re_data, safe=False)


# 添加修改设备信息
class AssetAddUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        print(request.data)
        if 'hostname' in request.data and 'lanip' in request.data and 'status' in request.data:
            hostname = request.data.get('hostname', None)
            lanip = request.data.get('lanip', None)
            wanip = request.data.get('wanip', None)
            status = request.data.get('status', None)
            functionIds = request.data.get('functionIds', None)
            itemId = request.data.get('itemId', None)
            summary = request.data.get('summary', None)
            try:
                item_query = Item.objects.filter(pk=itemId).first()
                sql = Asset.objects.create(hostname=hostname, lanip=lanip,wanip=wanip, status=status, functionIds=functionIds, summary=summary, itemId=item_query)
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
        if 'hostname' in request.data and 'lanip' in request.data and 'status' in request.data:
            id = request.data['id']
            hostname = request.data.get('hostname', None)
            lanip = request.data.get('lanip', None)
            wanip = request.data.get('wanip', None)
            status = request.data.get('status', None)
            functionIds = request.data.get('functionIds', None)
            itemId = request.data.get('itemId', None)
            summary = request.data.get('summary', None)
            # 更新数据
            try:
                item_query = Item.objects.filter(pk=itemId).first()
                Asset.objects.filter(pk=id).update(hostname=hostname, lanip=lanip, wanip=wanip, status=status,
                                           functionIds=functionIds, summary=summary, itemId=item_query, updateDate=datetime.now())
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


# 获取删除设备信息
class AssetGetDelView(APIView):
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        try:
            asset_query = Asset.objects.filter(pk=id).first()
            asset_ser = AssetSerializer(asset_query)
            re_data['data'] = asset_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def delete(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:
            Asset.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询设备列表
class DomainSearchView(APIView):

    def post(self, request,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        '''
        { code: 1, name: '设备名称' },
        { code: 2, name: '内网IP' },
        { code: 3, name: '外网IP' },
        '''
        query_select = {1: 'name__contains'}
        if 'current' in request.data and 'size' in request.data:
            # params修改为可写状态
            request.query_params._mutable = True
            current = request.data['current']
            size = request.data['size']
            name = request.data.get('name', None)
            itemId = request.data.get('itemId', None)
            search_dict = dict()
            if name:
                search_dict[query_select[1]] = name
            if itemId and len(itemId):
                search_dict['itemId'] = itemId
            if name or itemId:
                domain_query = Domain.objects.filter(**search_dict).order_by("id")
            else:
                domain_query = Domain.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = domain_query.count()
            page = MyPageNumber()
            page_Lable = page.paginate_queryset(queryset=domain_query, request=request, view=self)
            asset_ser = DomainSerializer(instance=page_Lable, many=True)
            print(asset_ser.data)
            re_data['data']['total'] = total
            re_data['data']['records'] = asset_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'
        return JsonResponse(re_data, safe=False)


# 添加修改域名信息
class DomainAddUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        print(request.data)
        if 'name' in request.data and 'itemId' in request.data:
            name = request.data.get('name', None)
            itemId = request.data.get('itemId', None)
            cname = request.data.get('cname', None)
            elb = request.data.get('elb', None)
            assetIds = request.data.get('assetIds', None)
            remark = request.data.get('remark', None)
            try:
                item_query = Item.objects.filter(pk=itemId).first()
                sql = Domain.objects.create(name=name, itemId=item_query, cname=cname, elb=elb,
                                            assetIds=assetIds, remark=remark)
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
        if 'name' in request.data and 'itemId':
            id = request.data['id']
            name = request.data.get('name', None)
            itemId = request.data.get('itemId', None)
            cname = request.data.get('cname', None)
            elb = request.data.get('elb', None)
            assetIds = request.data.get('assetIds', None)
            if len(assetIds) == 0:
                assetIds=[]
            remark = request.data.get('remark', None)
            # 更新数据
            try:
                item_query = Item.objects.filter(pk=itemId).first()
                Domain.objects.filter(pk=id).update(name=name, itemId=item_query, cname=cname, elb=elb,
                                           assetIds=assetIds, remark=remark)
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


# 获取删除设备信息
class DomainGetDelView(APIView):
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        try:
            domain_query = Domain.objects.filter(pk=id).first()
            domain_ser = DomainSerializer(domain_query)
            re_data['data'] = domain_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    def delete(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:
            Domain.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)



# 查询设备列表
class DomainAssetListView(APIView):

    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        asset_data = []
        try:
            assetIds = Domain.objects.get(pk=id).assetIds
            asset_list = re.findall(r"\d", assetIds)
            for assetId in asset_list:
                asset_query = Asset.objects.filter(id=int(assetId))
                asset_ser = AssetSerializer(instance=asset_query, many=True)
                asset_data.append(asset_ser.data[0])
            re_data['data']['assetList'] = asset_data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)
