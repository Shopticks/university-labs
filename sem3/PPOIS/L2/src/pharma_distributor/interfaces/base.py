from abc import ABC, abstractmethod
from typing import Any, List, TypeVar, Generic, Optional

T = TypeVar('T')


class IRepository(ABC, Generic[T]):

    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        ...

    @abstractmethod
    def save(self, entity: T) -> None:
        ...

    @abstractmethod
    def delete(self, id: Any) -> None:
        ...

    @abstractmethod
    def list_all(self) -> List[T]:
        ...


class INotificationService(ABC):

    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str) -> None:
        ...

    @abstractmethod
    def send_sms(self, phone: str, message: str) -> None:
        ...


class IPaymentGateway(ABC):

    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_token: str) -> bool:
        ...