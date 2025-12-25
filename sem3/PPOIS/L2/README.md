Credentials 4 2 -> 
User 6 5 -> Role, ContactInfo, Credentials
SecurityService 1 2 -> BaseRepository, User, Role
Category 4 2 -> 
ProductSpecification 4 1 -> Volume
BaseProduct 7 5 -> Money, Category, ProductSpecification
Medicine 4 4 -> 
MedicalDevice 5 5 -> WarrantyStatus
Currency 3 0 -> 
VolumeUnit 4 0 ->
WeightUnit 3 0 ->
Role 4 0 ->
OrderStatus 5 0 ->
WarrantyStatus 3 0 ->
VehicleStatus 3 0 ->
DriverStatus 3 0 ->
RouteStatus 4 0 ->
Address 4 0 ->
ContactInfo 3 0 ->
Volume 2 1 -> VolumeUnit
Money 2 1 -> Currency
BankAccount 4 3 -> Money
Transaction 6 0 -> Money
FinanceService 0 1 -> CurrencyConverter
BaseRepository 0 4 ->
BaseNotificationService 0 2 ->
BasePaymentGateway 0 1 ->
BaseConverter 0 1 ->
BaseCurrencyConverter 0 2 -> BaseConverter
BaseDimensionConverter 0 2 -> BaseConverter
BaseValidator 0 1 ->
StockBatch 7 4 -> Volume
Warehouse 6 9 -> Address, Volume, StockBatch
Supplier 4 0 ->
InventoryManager 0 6 -> Warehouse, BaseProduct, StockBatch
Driver 5 5 -> DriverStatus
VehicleStats 4 0 ->
Vehicle 8 10 -> VehicleStatus, Driver
RoutePoint 5 1 -> Address
DeliveryRoute 7 5 -> Vehicle, RoutePoint
FinancialSummary 7 0 -> Currency
BatchReportItem 5 0 ->
InventoryLineItem 7 0 -> Currency, BatchReportItem
InventoryReport 7 0 -> Currency, InventoryLineItem
SalesPerformanceItem 3 0 ->
ReportGenerator 0 3 -> Order, Currency, CatalogService, CurrencyConverter, FinancialSummary, OrderStatus, InventoryReport, Warehouse, SalesPerformanceItem
Customer 5 0 -> Address
OrderItem 3 1 -> BaseProduct, Money
Order 6 7 -> Customer, OrderItem, Money, BaseProduct, OrderStatus
SalesService 0 3 -> InventoryManager, BaseProduct, Customer, Warehouse, Order
PharmaError 0 0 ->
ValidationError 0 0 -> PharmaError
AuthenticationError 0 0 -> PharmaError
UserPermissionError 0 0 -> AuthenticationError
FinanceError 0 0 -> PharmaError
InsufficientFundsError 0 0 -> FinanceError
CurrencyMismatchError 0 0 -> FinanceError
InventoryError 0 0 -> PharmaError
OutOfStockError 0 0 -> InventoryError
WarehouseFullError 0 0 -> InventoryError
LogisticsError 0 0 -> PharmaError
RouteNotFoundError 0 0 -> LogisticsError
SalesError 0 0 -> PharmaError
ContractExpiredError 0 0 -> SalesError
InvalidOrderStatusError 0 0 -> SalesError
ReporterError 0 0 -> PharmaError