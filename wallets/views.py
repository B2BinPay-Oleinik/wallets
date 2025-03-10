from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_json_api.views import (
    AutoPrefetchMixin,
    ModelViewSet,
    PreloadIncludesMixin,
    RelatedMixin,
)

from wallets.models import Transaction, Wallet
from wallets.serializers import TransactionSerializer, WalletSerializer


class WalletViewSet(ModelViewSet):
    """ViewSet for viewing and editing wallets."""

    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    filterset_fields = {
        'label': ('exact', 'contains', 'iexact', 'icontains'),
        'balance': ('exact', 'gte', 'lte'),
    }
    ordering_fields = ('id', 'balance', 'label')
    ordering = ('id',)


class TransactionViewSet(
    AutoPrefetchMixin,
    PreloadIncludesMixin,
    RelatedMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """ViewSet for viewing and editing transactions."""

    http_method_names = ["get", "post", "head", "options"]
    queryset = Transaction.objects.select_related('wallet')
    serializer_class = TransactionSerializer

    filterset_fields = {
        'amount': ('exact', 'gte', 'lte'),
        'wallet': ('exact',),
        'txid': ('exact',),
    }
    ordering_fields = ('id', 'amount')
    ordering = ('-id',)

    def create(self, request: Request, *args: object, **kwargs: object) -> Response:
        """Create a new transaction."""
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as exc:
            raise ValidationError(detail=exc) from exc
