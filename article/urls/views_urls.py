from django.urls import path
from article import views

__all__ = ["urlpatterns"]

app_name = "article"

urlpatterns = [
    # path(r'login/', views.LoginView.as_view(), name='user_login'),
    path(r'category/search/', views.CategorySearchView.as_view(), name='category_search'),
]