from rest_framework_json_api.relations import ResourceRelatedField
from rest_framework_json_api.serializers import ModelSerializer

from wallets.models import Transaction, Wallet


class WalletSerializer(ModelSerializer):
    """Serializer for the Wallet model."""

    transactions = ResourceRelatedField(
        model=Transaction,
        many=True,
        read_only=True,
    )

    class Meta:
        """Serializer metadata."""
        model = Wallet
        fields = ('label', 'balance', 'transactions')
        read_only_fields = ('id', 'balance', 'transactions')


class TransactionSerializer(ModelSerializer):
    """Serializer for the Transaction model."""

    wallet = ResourceRelatedField(
        model=Wallet,
        required=True,
        queryset=Wallet.objects.all(),
    )

    class Meta:
        """Serializer metadata."""
        model = Transaction
        fields = ('txid', 'amount', 'wallet')
        read_only_fields = ('id', 'txid')

    included_serializers = {'wallet': WalletSerializer}

    class JSONAPIMeta:
        """JSON:API metadata."""
        included_resources = ['wallet']
