from django.urls import path
from system import views

__all__ = ["urlpatterns"]

app_name = "system"

urlpatterns = [
    path(r'menu/user/<int:userid>', views.MenuUserList.as_view(), name='menu_list'),
    path(r'menu/user2/<int:userid>', views.MenuUserList2.as_view(), name='menu_list'),
    path(r'user/search/', views.UserSearchView.as_view(), name='user_search'),
    path(r'user/', views.UserAddUpdateView.as_view(), name='user_add_update'),
    path(r'user/<int:userid>', views.UserGetDelView.as_view(), name='user_get_update'),
    path(r'user/password/', views.UserPasswordView.as_view(), name='user_password'),
    path(r'user/<int:id>/role/ids/', views.UserRoleListView.as_view(), name='user_role_list'),
    path(r'user/<int:id>/role/save/', views.UserRoleSaveView.as_view(), name='user_role_save'),
    # 权限路劲
    path(r'role/search/', views.RoleSearchView.as_view(), name='role_search'),
    path(r'role/', views.RoleAddUpdateView.as_view(), name='role_add_update'),
    path(r'role/<int:id>', views.RoleGetDelView.as_view(), name='role_get_update'),
    path(r'role/<int:id>/menu/ids/', views.RoleMenuListView.as_view(), name='role_menu_list'),
    path(r'role/<int:id>/menu/save/', views.RoleMenuSaveView.as_view(), name='role_menu_save'),

    # 获取菜单
    path(r'menu/', views.MenuAddUpdateView.as_view(), name='menu_add_update'),
    path(r'menu/search/', views.MenuSearchView.as_view(), name='menu_search'),
    path(r'menu/<int:id>', views.MenuGetDelView.as_view(), name='menu_get_update'),

    # 系统所有权限列表
    path(r'menu/permlist/', views.PermissionListView.as_view(), name='permission_list'),
]
