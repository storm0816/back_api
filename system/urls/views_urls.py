from django.urls import path
from system import views

__all__ = ["urlpatterns"]

app_name = "system"

urlpatterns = [
    path(r'menu/user/<int:userid>', views.MenuUserList.as_view(), name='menu_list'),
]