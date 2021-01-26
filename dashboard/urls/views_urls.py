from django.urls import path
from dashboard import views

__all__ = ["urlpatterns"]

app_name = "dashboard"

urlpatterns = [
    # 项目
    path(r'dashboard/search/', views.DashboardSearchView.as_view(), name='item_search'),
]