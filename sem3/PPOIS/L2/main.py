from datetime import date, timedelta
from decimal import Decimal
from typing import TypeVar, List, Optional, Any

from pharma_distributor.catalog import CatalogService, Medicine, Category, ProductSpecification
from pharma_distributor.common import Address, ContactInfo, Volume, Currency, VolumeUnit
from pharma_distributor.finance import Money
from pharma_distributor.interfaces import BaseRepository
from pharma_distributor.inventory import InventoryManager, Warehouse
from pharma_distributor.reporting import ReportGenerator
from pharma_distributor.sales import Customer, SalesService


# Some simple database implemetation
T = TypeVar("T")


class InMemoryRepository(BaseRepository[T]):
    def __init__(self):
        self._store = {}

    def get(self, id: Any) -> Optional[T]:
        return self._store.get(id)

    def save(self, entity: Any) -> None:
        self._store[entity.id] = entity

    def delete(self, id: Any) -> None:
        if id in self._store:
            del self._store[id]

    def list_all(self) -> List[T]:
        return list(self._store.values())


def main():
    print("=== Run Pharma Distributor System ===\n")

    # Initialize database
    product_repo = InMemoryRepository()

    # Initialize services
    inventory_manager = InventoryManager()
    catalog_service = CatalogService(product_repository=product_repo)
    sales_service = SalesService(inventory_manager=inventory_manager)
    report_generator = ReportGenerator(catalog_service=catalog_service)

    print("1. [Catalog] Creating categories and products...")

    cat_painkillers = Category(id=1, name="Painkillers", description="Pain relief")
    specs = ProductSpecification(
        manufacturer="Bayer",
        country_of_origin="Germany",
        storage_conditions="Dry place < 25C",
        packaging_volume=Volume(Decimal("0.001"), VolumeUnit.CUBIC_METER)
    )

    aspirin = Medicine(
        id=101,
        name="Aspirin Cardio",
        price=Money(Decimal("15.50"), Currency.BYN),
        category=cat_painkillers,
        specs=specs,
        dosage="100mg",
        active_substance="Acetylsalicylic acid",
        is_prescription_required=False,
        expiry_date=date.today() + timedelta(days=365)
    )

    # Save medicine to the database
    catalog_service.register_product(aspirin)
    print(f"   -> The product is registered: {aspirin.get_display_info()}")

    # Some warehouse setup
    print("\n2. [Warehouse] Warehouse customisation and goods acceptance...")

    wh_address = Address("Belarus", "Minsk", "Prittyckogo 1", "220000")
    warehouse = Warehouse(
        id=1,
        name="Central Minsk",
        address=wh_address,
        capacity=Volume(Decimal("1000.0"), VolumeUnit.CUBIC_METER)
    )

    # We accept a batch of goods (for these example - about 100 packages)
    try:
        inventory_manager.receive_shipment(
            warehouse=warehouse,
            product=aspirin,
            quantity=100,
            batch_number="BATCH-001",
            expiry_date=aspirin.expiry_date
        )
        current_stock = inventory_manager.get_stock_level(warehouse, aspirin.id)
        print(f"   -> The party is accepted. Current stock balance: {current_stock} things")
    except Exception as e:
        print(f"   -> Acceptance error: {e}")
        return

    # Basic example for sales process
    print("\n3. [Sales] Ordering by customer...")

    customer = Customer(
        id=55,
        name="Pharmacy №5",
        billing_address=Address("Belarus", "Grodno", "Lenina 5", "230000"),
        shipping_address=Address("Belarus", "Grodno", "Lenina 5", "230000"),
        contact=ContactInfo("pharm5@example.com", "+375291112233")
    )

    # The client orders 20 packs of Aspirin
    order = sales_service.create_order(customer, [(aspirin, 20)])
    print(f"   -> Order was created: {order.id}. Status: {order.status.name}")

    # Order processing (goods reservation and payment)
    try:
        sales_service.process_order(order, warehouse)
        print(f"   -> The order is processed and paid. Status: {order.status.name}")

        new_stock = inventory_manager.get_stock_level(warehouse, aspirin.id)
        print(f"   -> Stock balance after reserve: {new_stock} things")

        # Ship our order
        order.ship()
        order.deliver()
        print(f"   -> The order has been delivered to the customer. Status: {order.status.name}")

    except Exception as e:
        print(f"   -> Order processing error: {e}")

    # Reporting example
    print("\n4. [Reporting] Financial report generation...")

    # generate basic report
    today = date.today()
    fin_report = report_generator.generate_financial_report(
        orders=[order],
        start=today,
        end=today,
        target_currency=Currency.BYN
    )

    print(f"   --- Financial report ---")
    print(f"   Total orders: {fin_report.total_orders_count}")
    print(f"   Total revenue: {fin_report.total_revenue} {fin_report.currency.value}")
    print(f"   Average check:   {fin_report.average_order_value} {fin_report.currency.value}")

    print("\n=== The work has been completed successfully ===")


if __name__ == "__main__":
    main()
