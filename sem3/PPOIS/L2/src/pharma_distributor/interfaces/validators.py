from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar('T')


class BaseValidator(ABC, Generic[T]):
    @abstractmethod
    def validate(self, value: T) -> None:
        ...