from django.urls import path
from assets import views

__all__ = ["urlpatterns"]

app_name = "assets"

urlpatterns = [
    # 项目
    path(r'item/search/', views.ItemSearchView.as_view(), name='item_search'),
    path(r'item/', views.ItemAddUpdateView.as_view(), name='item_add_update'),
    path(r'item/<int:id>', views.ItemGetDelView.as_view(), name='item_get_delete'),
    path(r'item/list/', views.ItemListView.as_view(), name='item_status_list'),
    path(r'item/function/list/', views.ItemFunctionListView.as_view(), name='item_function_list'),
    path(r'item/asset/list/<int:itemid>', views.ItemAssetListView.as_view(), name='item_asset_list'),
    # 功能
    path(r'function/search/', views.FunctionSearchView.as_view(), name='function_search'),
    path(r'function/', views.FunctionAddUpdateView.as_view(), name='function_add_update'),
    path(r'function/<int:id>', views.FunctionGetDelView.as_view(), name='function_get_delete'),
    # 设备
    path(r'asset/search/', views.AssetSearchView.as_view(), name='asset_search'),
    path(r'asset/', views.AssetAddUpdateView.as_view(), name='asset_add_update'),
    path(r'asset/<int:id>', views.AssetGetDelView.as_view(), name='asset_get_delete'),
    # 域名
    path(r'domain/search/', views.DomainSearchView.as_view(), name='domain_search'),
    path(r'domain/', views.DomainAddUpdateView.as_view(), name='domain_add_update'),
    path(r'domain/<int:id>', views.DomainGetDelView.as_view(), name='domain_get_delete'),
    path(r'domain/asset/list/<int:id>', views.DomainAssetListView.as_view(), name='domain_asset_list'),
]