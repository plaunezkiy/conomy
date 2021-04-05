from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

router = DefaultRouter()
router.register('wallets', views.WalletViewSet, basename='wallets')
router.register('transactions', views.TransactionViewSet, basename='transactions')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/token/', TokenObtainPairView.as_view(), name='obtain_token'),
    path('v1/token/refresh', TokenRefreshView.as_view(), name='refresh_token')
]
