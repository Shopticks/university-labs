from pharma_distributor.finance.models import Money, BankAccount, Transaction
from pharma_distributor.utils.converters import CurrencyConverter
from pharma_distributor.utils.generators import IDGenerator
from pharma_distributor.exceptions import FinanceError


class FinanceService:
    """
    Domain service for handling complex financial operations like transfers
    between accounts with potential currency conversion.
    """
    def __init__(self, converter: CurrencyConverter):
        """
        Args:
            converter: Service to handle currency exchange rate calculations.
        """
        self.converter = converter

    def transfer_funds(self, source: BankAccount, target: BankAccount, amount: Money) -> Transaction:
        """
        Transfers funds from the source account to the target account.
        Automatically handles currency conversion if accounts have different currencies.
        Implements basic rollback logic if the deposit fails.

        Args:
            source: The account to withdraw from.
            target: The account to deposit into.
            amount: The amount to withdraw (in source account's currency).

        Returns:
            Transaction: A record of the successful transfer.

        Raises:
            FinanceError: If the transfer fails during execution.
            InsufficientFundsError: If the source account lacks funds.
        """
        source.withdraw(amount)

        # Currency conversion, if necessary
        amount_to_deposit = amount
        if source.balance.currency != target.balance.currency:
            converted_val = self.converter.convert(
                amount.amount,
                amount.currency,
                target.balance.currency
            )
            amount_to_deposit = Money(converted_val, target.balance.currency)

        try:
            target.deposit(amount_to_deposit)
        except Exception as e:
            # Simple rollback mechanism
            source.deposit(amount)
            raise FinanceError(f"Transfer failed during deposit: {str(e)}")

        return Transaction(
            id=IDGenerator.generate_uuid(),
            source_account_id=source.iban,
            target_account_id=target.iban,
            amount=amount,
            description=f"Transfer from {source.bank_name} to {target.bank_name}"
        )