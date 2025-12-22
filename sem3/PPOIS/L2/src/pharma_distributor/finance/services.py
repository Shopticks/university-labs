from src.pharma_distributor.finance.models import Money, BankAccount, Transaction
from src.pharma_distributor.utils.converters import CurrencyConverter
from src.pharma_distributor.utils.generators import IDGenerator
from src.pharma_distributor.exceptions import FinanceError


class FinanceService:
    def __init__(self, converter: CurrencyConverter):
        self.converter = converter

    def transfer_funds(self, source: BankAccount, target: BankAccount, amount: Money) -> Transaction:
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
            source.deposit(amount)
            raise FinanceError(f"Transfer failed during deposit: {str(e)}")

        return Transaction(
            id=IDGenerator.generate_uuid(),
            source_account_id=source.iban,
            target_account_id=target.iban,
            amount=amount,
            description=f"Transfer from {source.bank_name} to {target.bank_name}"
        )