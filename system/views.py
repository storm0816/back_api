from rest_framework_jwt.views import APIView
from django.http import JsonResponse
from user.models import UserProfile as User
from user.models import Role
from .models import Menu
from django.contrib.auth.models import Permission
from user.serializers import UserSerializer, RoleSerializer
from .serializers import MenuSerializer, MenuGetSerializer, PermissionSerializer
from extend.MyPageNumber import MyPageNumber
#处理put请求
from django.http import QueryDict
# 临时数据
from extend.data import *
from django.contrib.auth.decorators import permission_required
from extend.base import method_decorator_adaptor, find, abridge
from rest_framework import status
from datetime import datetime



# Create your views here.

# 后台权限列表
class PermissionListView(APIView):

    def get(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        try:
            permission_list = Permission.objects.all()
            permission_ser = PermissionSerializer(instance=permission_list, many=True)
            re_data['data'] = permission_ser.data
            pass
        except Exception as ex:
            msg = "添加失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data)


class MenuUserList(APIView):

    def get(self, request, userid, *args, **kwargs):
        print(userid)
        res = {'code': 20000, 'message': '获取成功'}
        data = MenUserList()
        res['data'] = data
        return JsonResponse(res)

class MenuUserList2(APIView):

    def get(self, request, userid, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        button_list = []
        menutree_list = []
        try:
            user_query = User.objects.get(id=userid)
            role_query = user_query.groups.all().values_list('id', flat=True)
            role_list = list(role_query)
            menu_query = Menu.objects.filter(parentId=0).order_by("id")
            menu_ser = MenuSerializer(instance=menu_query, many=True)
            for roleid in role_list:
                role = Role.objects.filter(pk=roleid).first()
                perm_query = role.permissions.all().values_list('id', flat=True)
                perm_list = list(perm_query)
                for permissionId in perm_list:
                    menu_query = Menu.objects.filter(permissionId=permissionId).values_list('code', flat=True)
                    menu_code = list(menu_query)[0]
                    button_list.append(menu_code)
                    # 过滤数据中是否存在menu_code关键字
                    menu_find = find(menu_code, menu_ser.data)
                    if menu_find:
                        # 得到目录信息后，删除按钮信息
                        menu_find_abridge = abridge(menu_find)
                        menutree_list.append(menu_find_abridge)
                    else:
                        pass
                # 去重button_list
                button_list = list(set(button_list))
                re_data['data']['buttonList'] = button_list
                re_data['data']['menuTreeList'] = menutree_list
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询用户信息列表
class UserSearchView(APIView):
    @method_decorator_adaptor(permission_required, 'user.view_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
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
            if 'username' in request.data:
                if 'mobile' in request.data:
                    user_list = User.objects.filter(username__contains=request.data['username'],
                                                            mobile__contains=request.data['mobile']).order_by("id")
                else:
                    user_list = User.objects.filter(username__contains=request.data['username']).order_by("id")

            else:
                if 'mobile' in request.data:
                    user_list = User.objects.filter(mobile__contains=request.data['mobile']).order_by("id")
                else:
                    user_list = User.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = user_list.count()
            page = MyPageNumber()
            page_category = page.paginate_queryset(queryset=user_list, request=request, view=self)
            user_ser = UserSerializer(instance=page_category, many=True)
            print(user_ser.data)
            re_data['data']['total'] = total
            re_data['data']['records'] = user_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 添加与更新用户信息
class UserAddUpdateView(APIView):
    @method_decorator_adaptor(permission_required, 'user.add_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        if 'username' in request.data and 'nickName' in request.data and 'mobile' in request.data and 'isAccountNonExpired' in request.data:
            username = request.data.get('username', None)
            nickName = request.data.get('nickName', None)
            mobile = request.data.get('mobile', None)
            isAccountNonExpired = request.data.get('isAccountNonExpired', None)
            is_active = False
            if isAccountNonExpired:
                is_active = True
            email = request.data.get('email', None)
            try:
                sql = User.objects.create(username=username, nickname=nickName, mobile=mobile, email=email, is_active=is_active)
                sql.save()
            except Exception as ex:
                msg = "添加失败: {ex}".format(ex=ex)
                re_data['code'] = 40000
                re_data['message'] = msg
        else:
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    @method_decorator_adaptor(permission_required, 'user.change_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def put(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "更新成功"
        put = QueryDict(request.body)
        put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        put_dict = eval(put_str)  # 将str类型转换为字典类型
        if 'username' in request.data and 'nickName' in request.data and 'mobile' in request.data and 'isAccountNonExpired' in request.data:
            id = put_dict.get("id")  # 获取传递参数
            print('更新用户给ID：', id)
            username = put_dict.get('username')
            nickName = put_dict.get('nickName')
            mobile = put_dict.get('mobile')
            isAccountNonExpired = put_dict.get('isAccountNonExpired')
            is_active = False
            if isAccountNonExpired:
                is_active = True
            # 判断email是否提交
            # 更新数据
            if 'email' in request.data:
                email = put_dict.get('email')
                try:
                    User.objects.filter(pk=id).update(username=username, nickname=nickName, mobile=mobile, is_active=is_active,email=email)
                except Exception as ex:
                    msg = "更新失败: {ex}".format(ex=ex)
                    re_data['code'] = 40000
                re_data['message'] = msg
                return JsonResponse(re_data, safe=False)
            else:
                try:
                    User.objects.filter(pk=id).update(username=username, nickname=nickName, mobile=mobile, is_active=is_active)
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


# 获取与删除用户信息
class UserGetDelView(APIView):
    @method_decorator_adaptor(permission_required, 'user.view_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def get(self, request, userid,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询用户ID：', userid)
        try:
            user_list = User.objects.filter(pk=userid).first()
            user_ser = UserSerializer(user_list)
            re_data['data'] = user_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    @method_decorator_adaptor(permission_required, 'user.delete_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def delete(self, request, userid,  *args, **kwargs,):
        print('删除用户id:', userid)
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:
            User.objects.filter(pk=userid).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 更新用户密码
class UserPasswordView(APIView):
    @method_decorator_adaptor(permission_required, 'user.change_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def put(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "密码更新成功"
                   }
        msg = "密码更新成功"
        put = QueryDict(request.body)
        put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        put_dict = eval(put_str)  # 将str类型转换为字典类型
        print(put_dict)
        if 'userId' in request.data and 'newPassword' in request.data:
            uid = put_dict.get("userId")  # 获取传递参数
            print('密码更新用户ID：', uid)
            newPassword = put_dict.get('newPassword')
            # 更新数据
            try:
                user = User.objects.get(pk=uid)
                user.set_password(newPassword)
                user.save()
            except Exception as ex:
                msg = "密码更新失败: {ex}".format(ex=ex)
                re_data['code'] = 40000
            re_data['message'] = msg
            return JsonResponse(re_data, safe=False)
        else:
            msg = '密码更新失败，参数异常'
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 获取用户角色列表
class UserRoleListView(APIView):
    @method_decorator_adaptor(permission_required, 'user.view_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def get(self, request, id, *args, **kwargs):
        print('获取{0}用户角色信息'.format(id))
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询用户角色成功"
                   }
        try:
            user_query = User.objects.get(id=id)
            role_query = user_query.groups.all().values_list('id',flat=True)
            role_list = list(role_query)
            re_data['data'] = role_list
        except Exception as ex:
            msg = "查询用户角色失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 更新用户角色列表
class UserRoleSaveView(APIView):
    @method_decorator_adaptor(permission_required, 'user.add_userprofile', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, id, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询用户角色成功"
                   }
        print('获取{0}用户角色信息'.format(id))
        user_role_list = request.data
        user_query = User.objects.get(id=id)
        if len(user_role_list) > 0:
            for roleid in user_role_list:
                try:
                    user_query.groups.add(roleid)
                except Exception as ex:
                    msg = "用户添加角色失败: {ex}".format(ex=ex)
                    re_data['code'] = 40000
                    re_data['message'] = msg
        else:
            user_query.groups.clear()
        return JsonResponse(re_data, safe=False)


# 查询菜单列表
class MenuSearchView(APIView):
    @method_decorator_adaptor(permission_required, 'system.view_menu', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        try:
            if 'name' in request.data:
                menu_query = Menu.objects.filter(name__contains=request.data['name']).order_by("id")
            else:
                # 过滤掉不是第一的目录
                menu_query = Menu.objects.filter(parentId=0).order_by("id")
            menu_ser = MenuSerializer(instance=menu_query, many=True)
            re_data['data'] = menu_ser.data
        except Exception as ex:
            msg = "添加失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 添加与更新菜单
class MenuAddUpdateView(APIView):
    @method_decorator_adaptor(permission_required, 'system.add_menu', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        print(request.data)
        if 'parentId' in request.data and 'type' in request.data and 'name' in request.data and 'code' in request.data:
            parentId = request.data.get('parentId', None)
            name = request.data.get('name', None)
            code = request.data.get('code', None)
            type = request.data.get('type', None)
            url = request.data.get('url', None)
            icon = request.data.get('icon', None)
            sort = request.data.get('sort', None)
            remark = request.data.get('remark', None)
            permissionId = request.data.get('permissionId', None)
            try:
                sql = Menu.objects.create(parentId=parentId, type=type, name=name, code=code, url=url, icon=icon, sort=sort, remark=remark, permissionId=permissionId)
                sql.save()
            except Exception as ex:
                msg = "添加失败: {ex}".format(ex=ex)
                re_data['code'] = 40000
                re_data['message'] = msg
        else:
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    @method_decorator_adaptor(permission_required, 'system.change_menu', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def put(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "更新成功"
        put = QueryDict(request.body)
        put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        put_dict = eval(put_str)  # 将str类型转换为字典类型
        id = put_dict.get("id")  # 获取传递参数
        print('更新用户给ID：', id)
        name = put_dict.get('name', None)
        code = put_dict.get('code', None)
        type = put_dict.get('type', None)
        url = put_dict.get('url', None)
        icon = put_dict.get('icon', None)
        sort = put_dict.get('sort', None)
        remark = put_dict.get('remark', None)
        permissionId= put_dict.get('permissionId', None)
        try:
            Menu.objects.filter(pk=id).update(name=name, remark=remark, code=code, type=type,
                                              url=url, icon=icon, sort=sort, permissionId=permissionId, updateDate=datetime.now())
        except Exception as ex:
            msg = "更新失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
        re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 获取与删除角色信息
class MenuGetDelView(APIView):
    @method_decorator_adaptor(permission_required, 'system.view_menu', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询菜单ID：', id)
        try:
            menu_list = Menu.objects.filter(pk=id).first()
            menu_ser = MenuGetSerializer(menu_list)
            re_data['data'] = menu_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    @method_decorator_adaptor(permission_required, 'system.delete_menu', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def delete(self, request, id,  *args, **kwargs,):
        print('删除菜单id:', id)
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:
            Menu.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 查询角色信息列表
class RoleSearchView(APIView):
    @method_decorator_adaptor(permission_required, 'user.view_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        if 'current' in request.data and 'size' in request.data:
            # params修改为可写状态
            request.query_params._mutable = True
            current = request.data['current']
            size = request.data['size']
            print('查询角色所有数据')
            # 判断前端是否传了搜索字段
            # 前端查询字段为name
            if 'name' in request.data:
                role_list = Role.objects.filter(name__contains=request.data['name']).order_by("id")
            else:
                role_list = Role.objects.all().order_by("id")
            # 将自选写入params中
            request.query_params.setlist('current', [current])
            request.query_params.setlist('size', [size])
            # 总数
            total = role_list.count()
            page = MyPageNumber()
            page_category = page.paginate_queryset(queryset=role_list, request=request, view=self)
            role_ser = RoleSerializer(instance=page_category, many=True)
            print(role_ser.data)
            re_data['data']['total'] = total
            re_data['data']['records'] = role_ser.data
        else:
            re_data['code'] = 40000
            re_data['message'] = '查询失败'

        return JsonResponse(re_data, safe=False)


# 添加与更新角色信息
class RoleAddUpdateView(APIView):
    @method_decorator_adaptor(permission_required, 'user.add_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "添加失败，参数异常"
        print(request.data)
        if 'name' in request.data:
            name = request.data['name']
            # 判断email是否提交
            if 'remark' in request.data:
                remark = request.data['remark']
                try:
                    sql = Role.objects.create(name=name, remark=remark)
                    sql.save()
                except Exception as ex:
                    msg = "添加失败: {ex}".format(ex=ex)
                    re_data['code'] = 40000
                    re_data['message'] = msg
            else:
                try:
                    sql = Role.objects.create(name=name)
                    sql.save()
                except Exception as ex:
                    msg = "添加失败: {ex}".format(ex=ex)
                    re_data['code'] = 40000
                    re_data['message'] = msg
        else:
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    @method_decorator_adaptor(permission_required, 'user.change_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def put(self, request, *args, **kwargs):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "添加成功"
                   }
        msg = "更新成功"
        put = QueryDict(request.body)
        put_str = list(put.items())[0][0]  # 将获取的QueryDict对象转换为str 类型
        put_dict = eval(put_str)  # 将str类型转换为字典类型
        if 'name' in request.data:
            id = put_dict.get("id")  # 获取传递参数
            print('更新用户给ID：', id)
            name = put_dict.get('name')
            if 'remark' in request.data:
                remark = put_dict.get('remark')
                try:
                    Role.objects.filter(pk=id).update(name=name, remark=remark)
                except Exception as ex:
                    msg = "更新失败: {ex}".format(ex=ex)
                    re_data['code'] = 40000
                re_data['message'] = msg
                return JsonResponse(re_data, safe=False)
            else:
                try:
                    Role.objects.filter(pk=id).update(name=name)
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


# 获取与删除角色信息
class RoleGetDelView(APIView):
    @method_decorator_adaptor(permission_required, 'user.view_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('查询角色ID：', id)
        try:
            role_list = Role.objects.filter(pk=id).first()
            role_ser = RoleSerializer(role_list)
            re_data['data'] = role_ser.data
        except Exception as ex:
            msg = "查询失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

    @method_decorator_adaptor(permission_required, 'user.delete_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def delete(self, request, id,  *args, **kwargs,):
        print('删除角色id:', id)
        re_data = {"data": {},
                   "code": 20000,
                   "message": "删除成功"
                   }
        try:
            Role.objects.filter(pk=id).delete()
        except Exception as ex:
            msg = "删除失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 获取角色菜单列表
class RoleMenuListView(APIView):
    @method_decorator_adaptor(permission_required, 'user.view_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def get(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('获取角色ID：{0},菜单权限'.format(id))
        role = Role.objects.filter(pk=id).first()
        try:
            perm_query = role.permissions.all().values_list('id', flat=True)
            perm_list = list(perm_query)
            print(list)
            post_list = []
            for permissionId in perm_list:
                try:
                    menu_query = Menu.objects.filter(permissionId=int(permissionId)).values_list('id', flat=True)
                    menu_id = list(menu_query)[0]
                    post_list.append(menu_id)
                except Exception as ex:
                    msg = "查询角色按钮权限id失败: {ex}".format(ex=ex)
                    re_data['code'] = 40000
                    re_data['message'] = msg
            re_data['data'] = post_list
        except Exception as ex:
            msg = "查询角色All权限失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)


# 更新角色菜单列表
class RoleMenuSaveView(APIView):
    @method_decorator_adaptor(permission_required, 'user.change_role', login_url=None,
                              raise_exception=status.HTTP_403_FORBIDDEN)
    def post(self, request, id,  *args, **kwargs,):
        re_data = {"data": {},
                   "code": 20000,
                   "message": "查询成功"
                   }
        print('更新角色按钮权限id', id)
        # 前端上传的所有选这项（菜单，目录，按钮）
        post_list = request.data
        # 获取到所有按钮权限列表
        try:
            botton_query = Menu.objects.filter(type=3).values_list('id', flat=True)
            botton_list = list(botton_query)
            # 取交集，得到所需的按钮权限list
            menu_list = list(set(post_list).intersection(set(botton_list)))
            # 按钮对应的权限id
            per_list = []
            for menu in menu_list:
                perid_query = Menu.objects.filter(pk=menu).values_list('permissionId')
                perid = list(perid_query)[0][0]
                per_list.append(perid)
            # 给对应角色赋予权限
            role = Role.objects.get(pk=id)
            # 先清空角色权限，再赋予
            role.permissions.clear()
            for per_id in per_list:
                role.permissions.add(per_id)
        except Exception as ex:
            msg = "更新角色按钮权限失败: {ex}".format(ex=ex)
            re_data['code'] = 40000
            re_data['message'] = msg
        return JsonResponse(re_data, safe=False)

