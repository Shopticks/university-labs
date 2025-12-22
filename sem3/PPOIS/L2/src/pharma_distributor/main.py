# from decimal import Decimal
# from datetime import date
#
# # Imports (Models)
# from pharma_distributor.finance.models import Money, BankAccount
# from pharma_distributor.catalog.models import Medicine, Category, ProductSpecification
# from pharma_distributor.inventory.models import Warehouse
# from pharma_distributor.common.models import Address, ContactInfo
# from pharma_distributor.common.enums import Currency
#
# # Imports (Services)
# from pharma_distributor.finance.services import FinanceService
# from pharma_distributor.inventory.services import InventoryManager
# from pharma_distributor.catalog.services import CatalogService
# from pharma_distributor.utils.converters import CurrencyConverter
#
#
# def main():
#     print("=== Pharma Distributor System Starting ===")
#
#     # 1. Инициализация сервисов (DI Container в миниатюре)
#     currency_converter = CurrencyConverter()
#     finance_service = FinanceService(currency_converter)
#     inventory_manager = InventoryManager()
#     catalog_service = CatalogService()
#
#     # 2. Создание объектов-значений (Value Objects)
#     addr_minsk = Address("Belarus", "Minsk", "Nezavisimosti", "220000")
#     contact_info = ContactInfo("info@pharma.by", "+375291112233")
#
#     # 3. Финансы: Создание счетов
#     acc_source = BankAccount(
#         iban="BY12ALFA0000",
#         bank_name="Alfa",
#         balance=Money(Decimal("50000.00"), Currency.BYN)
#     )
#     acc_target = BankAccount(
#         iban="US88BOFA0000",
#         bank_name="BoA",
#         balance=Money(Decimal("1000.00"), Currency.USD)
#     )
#
#     print(f"Initial Balance Source: {acc_source.balance}")
#     print(f"Initial Balance Target: {acc_target.balance}")
#
#     # 4. Финансы: Перевод средств
#     try:
#         tx = finance_service.transfer_funds(
#             acc_source,
#             acc_target,
#             Money(Decimal("1000.00"), Currency.BYN)
#         )
#         print(f"Transaction successful: {tx.id}")
#         print(f"New Balance Source: {acc_source.balance}")
#         print(f"New Balance Target: {acc_target.balance} (Converted)")
#     except Exception as e:
#         print(f"Transaction failed: {e}")
#
#     # 5. Каталог: Создание товара
#     category_pain = Category(id=1, name="Painkillers")
#     specs = ProductSpecification("Pfizer", "USA", "Dry place")
#
#     aspirin = Medicine(
#         id=101,
#         name="Aspirin Cardio",
#         price=Money(Decimal("15.50"), Currency.BYN),
#         category=category_pain,
#         specs=specs,
#         dosage="100mg",
#         active_substance="Acetylsalicylic acid",
#         is_prescription_required=False,
#         expiry_date=date(2026, 1, 1)
#     )
#
#     # 6. Склад: Приемка товара
#     warehouse_main = Warehouse(
#         id=1,
#         name="Central Hub",
#         address=addr_minsk,
#         capacity_sq_m=1000.0
#     )
#
#     inventory_manager.add_stock(warehouse_main, aspirin, 500)
#     print(f"Warehouse stock for Product {aspirin.id}: {warehouse_main.stock.get(aspirin.id)}")
#
#     # 7. Проверка бизнес-логики
#     is_expired = catalog_service.check_expiration(aspirin)
#     print(f"Is Aspirin expired? {is_expired}")
#
#     print("=== System Shutdown ===")
#
#
# if __name__ == "__main__":
#     main()
