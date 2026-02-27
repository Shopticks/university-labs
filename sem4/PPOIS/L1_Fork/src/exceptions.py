class MetroSystemError(Exception): pass

# --- Tickets Errors---
class TicketError(MetroSystemError): pass
class TicketExpiredError(TicketError): pass
class TicketExhaustedError(TicketError): pass

# --- Turnstile Errors ---
class TurnstileError(MetroSystemError): pass
class TurnstileLockedError(TurnstileError): pass
class TurnstileAlreadyUnlockedError(TurnstileError): pass
class TurnstileLockedDownError(TurnstileError): pass

# -- Platform Errors ---
class PlatformError(MetroSystemError): pass
class PlatformOccupiedError(PlatformError): pass
class PlatformEmptyError(PlatformError): pass

# -- Station Errors ---
class StationError(MetroSystemError): pass

# --- Train Errors ---
class TrainError(MetroSystemError): pass
class TrainFullError(TrainError): pass
class TrainNotEmptyError(TrainError): pass
class TrainNeedsMaintenanceError(TrainError): pass