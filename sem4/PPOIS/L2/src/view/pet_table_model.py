from PySide6.QtCore import QAbstractTableModel, Qt
from src.model.pet_record import PetRecord

HEADERS = ["Имя питомца", "Дата рождения", "Дата посл. приёма", "ФИО ветеринара", "Диагноз"]


class PetTableModel(QAbstractTableModel):
    def __init__(self, records: list[PetRecord]):
        super().__init__()
        self._records = records

    def rowCount(self, parent=None):
        return len(self._records)

    def columnCount(self, parent=None):
        return 5

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return None
        r = self._records[index.row()]
        col = index.column()
        if col == 0: return r.pet_name
        if col == 1: return r.birth_date.strftime("%d.%m.%Y")
        if col == 2: return r.last_visit_date.strftime("%d.%m.%Y")
        if col == 3: return r.vet_name
        if col == 4: return r.diagnosis

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return HEADERS[section]
        return str(section + 1)