from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    CheckConstraint,
    DecimalField,
    ForeignKey,
    Model,
    Q,
    UUIDField,
)
from django.db.transaction import atomic


class Wallet(Model):
    """Model representing a wallet with a label and balance."""

    label = CharField(max_length=255)
    balance = DecimalField(
        max_digits=18,
        decimal_places=8,
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self) -> str:
        """Return string representation of the wallet."""
        return f"{self.label} (Balance: {self.balance})"

    class Meta:
        """Wallet model metadata."""
        constraints = [CheckConstraint(check=Q(balance__gte=0), name='balance_non_negative')]


class Transaction(Model):
    """Model representing a financial transaction linked to a wallet."""

    wallet = ForeignKey(Wallet, on_delete=CASCADE, related_name='transactions')
    txid = UUIDField(default=uuid4, unique=True, editable=False, db_index=True)
    amount = DecimalField(max_digits=18, decimal_places=8)

    @atomic
    def save(self, *args: object, **kwargs: object) -> None:
        """Save the transaction and update wallet balance."""
        self.wallet.balance += self.amount
        self.wallet.save()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Return string representation of the transaction."""
        return f"Transaction {self.txid} ({self.amount})"

    class Meta:
        """Transaction model metadata."""
        ordering = ['-id']
