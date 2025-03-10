from django.db import IntegrityError
from drf_spectacular.utils import extend_schema, extend_schema_view
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


@extend_schema_view(
    list=extend_schema(
        summary="List wallets",
        description="Get a paginated list of all wallets with their balances.",
        tags=["wallets"],
    ),
    create=extend_schema(
        summary="Create wallet",
        description="Create a new wallet with an initial balance of 0.",
        tags=["wallets"],
    ),
    retrieve=extend_schema(
        summary="Get wallet",
        description="Get details of a specific wallet by its ID.",
        tags=["wallets"],
    ),
    update=extend_schema(
        summary="Update wallet",
        description="Update a wallet's label.",
        tags=["wallets"],
    ),
    partial_update=extend_schema(
        summary="Partially update wallet",
        description="Update specific fields of a wallet.",
        tags=["wallets"],
    ),
    destroy=extend_schema(
        summary="Delete wallet",
        description="Delete a wallet and all its transactions.",
        tags=["wallets"],
    ),
)
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


@extend_schema_view(
    list=extend_schema(
        summary="List transactions",
        description="Get a paginated list of all transactions.",
        tags=["transactions"],
    ),
    create=extend_schema(
        summary="Create transaction",
        description="Create a new transaction. The wallet's balance will be updated automatically.",
        tags=["transactions"],
    ),
    retrieve=extend_schema(
        summary="Get transaction",
        description="Get details of a specific transaction by its ID.",
        tags=["transactions"],
    ),
)
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
