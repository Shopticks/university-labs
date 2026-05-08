import uuid
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


@dataclass
class PetRecord:
    pet_name: str
    birth_date: date
    last_visit_date: date
    vet_name: str
    diagnosis: str
    id: Optional[uuid.UUID] = field(default=None, compare=False)

    def is_empty(self) -> bool:
        return (
                self.pet_name == ""
            and self.birth_date == date.today()
            and self.last_visit_date == date.today()
            and self.vet_name == ""
            and self.diagnosis == ""
        )

    def is_valid(self) -> bool:
        return not self.validation_errors()

    def validation_errors(self) -> list[str]:
        errors = []
        if not self.pet_name:
            errors.append("Имя питомца")
        if not self.vet_name:
            errors.append("ФИО ветеринара")
        if not self.diagnosis:
            errors.append("Диагноз")
        return errors
