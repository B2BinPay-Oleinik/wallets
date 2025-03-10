from django.urls import include, path
from rest_framework.routers import DefaultRouter

from wallets.views import TransactionViewSet, WalletViewSet

router = DefaultRouter()
router.register('wallets', WalletViewSet)
router.register('transactions', TransactionViewSet)

urlpatterns = [path('api/', include(router.urls))]
