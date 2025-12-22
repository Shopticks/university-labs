class PharmaError(Exception):
    """
    Base exception for all application-specific errors in the Pharma Distributor system.
    """
    pass

class ValidationError(PharmaError):
    """
    Raised when input data fails business rule validation (e.g., negative quantity, invalid email).
    """
    pass

class AuthenticationError(PharmaError):
    """
    Raised when user identification fails (e.g., wrong password, user not found).
    """
    pass

class UserPermissionError(AuthenticationError):
    """
    Raised when an authenticated user attempts an action they are not authorized to perform.
    """
    pass

class FinanceError(PharmaError):
    """
    Base exception for errors related to financial operations.
    """
    pass

class InsufficientFundsError(FinanceError):
    """
    Raised when a bank account does not have enough balance to complete a withdrawal.
    """
    pass

class CurrencyMismatchError(FinanceError):
    """
    Raised when an operation attempts to combine or compare different currencies without conversion.
    """
    pass

class InventoryError(PharmaError):
    """
    Base exception for errors related to warehouse and stock management.
    """
    pass

class OutOfStockError(InventoryError):
    """
    Raised when a requested product quantity exceeds the available inventory.
    """
    pass

class WarehouseFullError(InventoryError):
    """
    Raised when a warehouse does not have enough physical capacity to accept a new shipment.
    """
    pass

class LogisticsError(PharmaError):
    """
    Base exception for errors related to fleet management, routing, and delivery.
    """
    pass

class RouteNotFoundError(LogisticsError):
    """
    Raised when a valid path or route cannot be calculated or found.
    """
    pass

class SalesError(PharmaError):
    """
    Base exception for errors related to order processing and customer management.
    """
    pass

class ContractExpiredError(SalesError):
    """
    Raised when an operation is attempted against an expired contract.
    """
    pass

class InvalidOrderStatusError(SalesError):
    """
    Raised when an illegal state transition is attempted on an order (e.g., shipping an unpaid order).
    """
    pass

class ReporterError(PharmaError):
    """
    Raised when report generation fails (e.g., due to data inconsistency or calculation errors).
    """
    pass