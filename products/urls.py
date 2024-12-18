from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ProductView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('product/register/', RegisterView.as_view(), name='product-register'),
    path('product/login/', LoginView.as_view(), name='product-login'),
    path('product/logout/', LogoutView.as_view(), name='product-logout'),
    path('product/operations/', ProductView.as_view(), name='product-operations'),
    path('product/token/refresh/', TokenRefreshView.as_view(), name='product-token-refresh'),
]
