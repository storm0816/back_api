from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

__all__ = ["urlpatterns"]

app_name = "user"

urlpatterns = [
    # path(r'login/', views.LoginView.as_view(), name='user_login'),
    path(r'login/', views.MyTokenObtainPairView.as_view(), name='user_login'),
    path(r'info/', views.HelloView.as_view(), name='user_info'),
    path(r'token/', views.TokenView.as_view(), name='token_get'),
    path(r'refresh/', views.MyTokenRefreshView.as_view(), name='token_refresh')
]