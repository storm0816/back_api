from django.urls import path
from article import views

__all__ = ["urlpatterns"]

app_name = "article"

urlpatterns = [
    # path(r'login/', views.LoginView.as_view(), name='user_login'),
    # 分类
    path(r'category/search/', views.CategorySearchView.as_view(), name='category_search'),
    path(r'category/', views.CategoryAddUpdateView.as_view(), name='category_add_update'),
    path(r'category/<int:id>', views.CategoryGetDelView.as_view(), name='category_get_delete'),
    path(r'category/list/', views.CategoryListView.as_view(), name='category_status_list'),
    path(r'category/label/list/', views.CategoryLabelListView.as_view(), name='category_label_list'),
    # 标签
    path(r'label/search/', views.LabelSearchView.as_view(), name='label_search'),
    path(r'label/', views.LabelAddUpdateView.as_view(), name='label_add_update'),
    path(r'label/<int:id>', views.LabelGetDelView.as_view(), name='label_get_delete'),
    # 文章
    path(r'article/search/', views.ArticleSearchView.as_view(), name='article_search'),
    path(r'article/article/<int:id>', views.ArticleDetailView.as_view(), name='article_detail'),
]