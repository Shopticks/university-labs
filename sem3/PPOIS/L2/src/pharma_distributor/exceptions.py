class PharmaError(Exception):
    """Base exception."""
    pass

class ValidationError(PharmaError): pass
class AuthenticationError(PharmaError): pass
class UserPermissionError(AuthenticationError): pass

class FinanceError(PharmaError): pass
class InsufficientFundsError(FinanceError): pass
class CurrencyMismatchError(FinanceError): pass

class InventoryError(PharmaError): pass
class OutOfStockError(InventoryError): pass
class WarehouseFullError(InventoryError): pass

class LogisticsError(PharmaError): pass
class RouteNotFoundError(LogisticsError): pass

class SalesError(PharmaError): pass
class ContractExpiredError(SalesError): pass
class InvalidOrderStatusError(SalesError): pass

class ReporterError(PharmaError): pass