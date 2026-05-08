from __future__ import annotations

from enum import Enum, auto

from PySide6.QtCore import QDate
from PySide6.QtWidgets import QDialog, QMessageBox, QHeaderView, QSpinBox, QDateEdit

from src.model.pet_record import PetRecord
from src.view.pet_table_model import PetTableModel
from src.ui_record_dialog import Ui_RecordDialog


class DialogMode(Enum):
    ADD    = auto()   # Добавить запись   — все 5 полей обязательны
    SEARCH = auto()   # Поиск записей     — селектор группы + таблица результатов
    DELETE = auto()   # Удалить записи    — селектор группы, без таблицы


_TITLES = {
    DialogMode.ADD:    "Добавить запись",
    DialogMode.SEARCH: "Поиск записей",
    DialogMode.DELETE: "Удалить записи",
}

_CONFIRM_BTN = {
    DialogMode.ADD:    "Добавить",
    DialogMode.SEARCH: "Найти",
    DialogMode.DELETE: "Удалить",
}

# Группы критериев: индекс в QComboBox criteriaGroup -> номера строк formLayout
_GROUP_NAME_BIRTH = 0
_GROUP_VISIT_VET  = 1
_GROUP_DIAG       = 2

# Строки formLayout: 0 — criteriaGroup, 1..5 — поля записи.
_ROW_CRITERIA = 0
_ROW_NAME, _ROW_BIRTH, _ROW_VISIT, _ROW_VET, _ROW_DIAG = 1, 2, 3, 4, 5
_FIELD_ROWS = (_ROW_NAME, _ROW_BIRTH, _ROW_VISIT, _ROW_VET, _ROW_DIAG)

_GROUP_ROWS = {
    _GROUP_NAME_BIRTH: (_ROW_NAME, _ROW_BIRTH),
    _GROUP_VISIT_VET:  (_ROW_VISIT, _ROW_VET),
    _GROUP_DIAG:       (_ROW_DIAG,),
}


class RecordDialog(QDialog):
    _PER_PAGE_DEFAULT = 10

    def __init__(self, mode: DialogMode, parent=None):
        super().__init__(parent)
        self._mode = mode
        self._results: list[PetRecord] = []
        self._current_page = 1
        self._per_page = self._PER_PAGE_DEFAULT

        self.ui = Ui_RecordDialog()
        self.ui.setupUi(self)

        self._apply_mode()
        self._connect_signals()

    def get_record(self) -> PetRecord:
        return PetRecord(
            pet_name=self.ui.fldName.text().strip(),
            birth_date=self.ui.fldBirth.date().toPython(),
            last_visit_date=self.ui.fldVisit.date().toPython(),
            vet_name=self.ui.fldVet.text().strip(),
            diagnosis=self.ui.fldDiag.text().strip(),
        )

    def get_criteria(self) -> dict:
        group = self.ui.criteriaGroup.currentIndex()
        if group == _GROUP_NAME_BIRTH:
            return {
                "pet_name": self.ui.fldName.text().strip(),
                "birth_date": self.ui.fldBirth.date().toPython(),
            }
        if group == _GROUP_VISIT_VET:
            return {
                "last_visit_date": self.ui.fldVisit.date().toPython(),
                "vet_name": self.ui.fldVet.text().strip(),
            }
        return {"diagnosis_phrase": self.ui.fldDiag.text().strip()}

    def show_results(self, records: list[PetRecord]) -> None:
        if self._mode != DialogMode.SEARCH:
            return
        self._results = records
        self._current_page = 1
        self._refresh_table()

    @staticmethod
    def _fix_calendar_spinbox(date_edit: QDateEdit) -> None:
        cal = date_edit.calendarWidget()
        for sb in cal.findChildren(QSpinBox):
            sb.setFixedWidth(72)

    def _apply_mode(self):
        self._fix_calendar_spinbox(self.ui.fldBirth)
        self._fix_calendar_spinbox(self.ui.fldVisit)

        self.setWindowTitle(_TITLES[self._mode])
        self.ui.lblTitle.setText(_TITLES[self._mode])
        self.ui.btnConfirm.setText(_CONFIRM_BTN[self._mode])

        self.ui.fldName.setPlaceholderText("Введите имя")
        self.ui.fldVet.setPlaceholderText("Введите ФИО")

        if self._mode == DialogMode.ADD:
            today = QDate.currentDate()
            self.ui.fldBirth.setDate(today)
            self.ui.fldVisit.setDate(today)
            self.ui.lblFormSection.setText("Данные записи")
            self.ui.formLayout.setRowVisible(_ROW_CRITERIA, False)
            self.ui.fldDiag.setPlaceholderText("Введите диагноз")
            for row in _FIELD_ROWS:
                self.ui.formLayout.setRowVisible(row, True)
            self.setMinimumSize(900, 550)
            self.resize(900, 550)
        else:
            self.ui.fldBirth.setDate(QDate(2020, 1, 1))
            self.ui.fldVisit.setDate(QDate(2025, 1, 1))
            self.ui.fldBirth.setToolTip("Точная дата рождения (день, месяц, год)")
            self.ui.fldVisit.setToolTip("Точная дата последнего приёма")

            self.ui.lblFormSection.setText("Критерии поиска")
            self.ui.formLayout.setRowVisible(_ROW_CRITERIA, True)
            self.ui.fldDiag.setPlaceholderText("Фраза из диагноза")
            self._apply_group(self.ui.criteriaGroup.currentIndex())

            header = self.ui.resultsTable.horizontalHeader()
            header.setSectionResizeMode(QHeaderView.Stretch)

            if self._mode == DialogMode.SEARCH:
                self.ui.resultsFrame.setVisible(True)
                self._refresh_table()
                self.setMinimumSize(900, 550)
                self.resize(1100, 720)
            else:
                self.ui.resultsFrame.setVisible(False)
                self.setMinimumSize(640, 360)
                self.resize(700, 400)

    def _apply_group(self, group: int):
        visible_rows = set(_GROUP_ROWS.get(group, ()))
        for row in _FIELD_ROWS:
            self.ui.formLayout.setRowVisible(row, row in visible_rows)

    def _connect_signals(self):
        self.ui.btnCancel.clicked.connect(self.reject)
        self.ui.btnConfirm.clicked.connect(self._on_confirm)

        if self._mode != DialogMode.ADD:
            self.ui.criteriaGroup.currentIndexChanged.connect(self._on_group_changed)
            self.ui.btnFirst.clicked.connect(self._go_first)
            self.ui.btnPrev.clicked.connect(self._go_prev)
            self.ui.btnNext.clicked.connect(self._go_next)
            self.ui.btnLast.clicked.connect(self._go_last)
            self.ui.spinPerPage.valueChanged.connect(self._on_per_page_changed)

    def _on_group_changed(self, index: int):
        self._apply_group(index)
        if self._mode == DialogMode.SEARCH:
            self._results = []
            self._current_page = 1
            self._refresh_table()

    def _on_confirm(self):
        if errors := self._get_validation_errors():
            QMessageBox.warning(
                self.parent(),
                "Заполните поля",
                "Обязательные поля не заполнены:\n• " + "\n• ".join(errors),
            )
            return
        self.accept()

    def _get_validation_errors(self) -> list[str]:
        if self._mode == DialogMode.ADD:
            errors = []
            if not self.ui.fldName.text().strip():
                errors.append("Имя питомца")
            if not self.ui.fldVet.text().strip():
                errors.append("ФИО ветеринара")
            if not self.ui.fldDiag.text().strip():
                errors.append("Диагноз")
            return errors

        group = self.ui.criteriaGroup.currentIndex()
        errors = []
        if group == _GROUP_NAME_BIRTH:
            if not self.ui.fldName.text().strip():
                errors.append("Имя питомца")
        elif group == _GROUP_VISIT_VET:
            if not self.ui.fldVet.text().strip():
                errors.append("ФИО ветеринара")
        elif group == _GROUP_DIAG:
            if not self.ui.fldDiag.text().strip():
                errors.append("Фраза из диагноза")
        return errors


    def _total_pages(self) -> int:
        return max(1, -(-len(self._results) // self._per_page))

    def _refresh_table(self):
        total = len(self._results)
        total_pages = self._total_pages()
        self._current_page = max(1, min(self._current_page, total_pages))

        start = (self._current_page - 1) * self._per_page
        model = PetTableModel(self._results[start:start + self._per_page])
        self.ui.resultsTable.setModel(model)

        self.ui.lblPageInfo.setText(f"Стр. {self._current_page} / {total_pages}")
        self.ui.lblTotal.setText(f"Всего: {total}")
        self.ui.btnFirst.setEnabled(self._current_page > 1)
        self.ui.btnPrev.setEnabled(self._current_page > 1)
        self.ui.btnNext.setEnabled(self._current_page < total_pages)
        self.ui.btnLast.setEnabled(self._current_page < total_pages)

    def _go_first(self):
        self._current_page = 1
        self._refresh_table()

    def _go_prev(self):
        self._current_page = max(1, self._current_page - 1)
        self._refresh_table()

    def _go_next(self):
        self._current_page = min(self._total_pages(), self._current_page + 1)
        self._refresh_table()

    def _go_last(self):
        self._current_page = self._total_pages()
        self._refresh_table()

    def _on_per_page_changed(self, value: int):
        self._per_page = value
        self._current_page = 1
        self._refresh_table()
