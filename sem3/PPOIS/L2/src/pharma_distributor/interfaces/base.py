from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic, Optional

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """
    Generic interface for Data Access Objects (DAOs) or Repositories.
    Provides standard CRUD operations for domain entities.
    """

    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        """
        Retrieves an entity by its unique identifier.

        Args:
            id: The unique identifier of the entity.

        Returns:
            Optional[T]: The entity if found, None otherwise.
        """
        ...

    @abstractmethod
    def save(self, entity: T) -> None:
        """
        Persists an entity (create or update).

        Args:
            entity: The entity to save.
        """
        ...

    @abstractmethod
    def delete(self, id: Any) -> None:
        """
        Removes an entity from the repository by its ID.

        Args:
            id: The unique identifier of the entity to remove.
        """
        ...

    @abstractmethod
    def list_all(self) -> List[T]:
        """
        Retrieves all entities stored in the repository.

        Returns:
            List[T]: A list of all entities.
        """
        ...


class INotificationService(ABC):
    """
    Abstract interface for sending notifications to users via different channels.
    """

    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        """
        Sends an email notification.

        Args:
            to_email: Recipient email address.
            subject: Email subject line.
            body: Email content body.
        """
        ...

    @abstractmethod
    def send_sms(self, phone: str, message: str) -> None:
        """
        Sends an SMS notification.

        Args:
            phone: Recipient phone number.
            message: Text message content.
        """
        ...


class IPaymentGateway(ABC):
    """
    Abstract interface for processing financial payments through external providers.
    """

    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_token: str) -> bool:
        """
        Processes a payment transaction.

        Args:
            amount: The monetary amount to charge.
            currency: The currency code (e.g., 'USD').
            card_token: The tokenized payment credential.

        Returns:
            bool: True if payment was successful, False otherwise.
        """
        ...