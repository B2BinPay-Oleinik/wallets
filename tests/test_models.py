from decimal import Decimal

from django.db import IntegrityError
from pytest import fixture, mark, raises

from wallets.models import Transaction, Wallet


@fixture
def wallet() -> Wallet:
    """Create a test wallet with initial balance."""
    return Wallet.objects.create(
        label="Test Wallet", balance=Decimal("100.00000000"),
    )


@mark.django_db
class TestTransaction:
    """Test the Transaction model."""
    def test_positive_transaction_succeeds(self, wallet: Wallet) -> None:
        """Test that a transaction that keeps balance positive succeeds."""
        Transaction(wallet=wallet, amount=Decimal("-50.00000000")).save()

        wallet.refresh_from_db()
        assert wallet.balance == Decimal("50.00000000")

    def test_negative_balance_fails(self, wallet: Wallet) -> None:
        """Test that a transaction that would make balance negative fails."""
        with raises(
            IntegrityError,
            match=(
                'new row for relation "wallets_wallet" violates '
                'check constraint "balance_non_negative"'
            ),
        ):
            Transaction(wallet=wallet, amount=Decimal("-150.00000000")).save()

        wallet.refresh_from_db()
        assert wallet.balance == Decimal("100.00000000")

    def test_multiple_transactions_respect_balance(self, wallet: Wallet) -> None:
        """Test that multiple transactions properly update the balance."""
        Transaction.objects.create(wallet=wallet, amount=Decimal("-30.00000000"))
        Transaction.objects.create(wallet=wallet, amount=Decimal("20.00000000"))

        wallet.refresh_from_db()
        assert wallet.balance == Decimal("90.00000000")

    def test_transaction_str(self, wallet: Wallet) -> None:
        """Test the __str__ method of the Transaction model."""
        transaction = Transaction(wallet=wallet, amount=Decimal("-50.00000000"))
        assert str(transaction) == f"Transaction {transaction.txid} (-50.00000000)"


@mark.django_db
class TestWallet:
    """Test the Wallet model."""
    def test_wallet_str(self, wallet: Wallet) -> None:
        """Test the __str__ method of the Wallet model."""
        assert str(wallet) == "Test Wallet (Balance: 100.00000000)"
