from pathlib import Path

from PySide6.QtWidgets import QMainWindow, QTreeWidgetItem, QMessageBox, QFileDialog
from PySide6.QtCore import Signal, QSize
from PySide6.QtGui import QIcon, QCloseEvent

from src.ui_mainwindow import Ui_MainWindow
from src.view.record_dialog import RecordDialog, DialogMode

class MainWindow(QMainWindow):
    add_requested = Signal()
    search_requested = Signal()
    delete_requested = Signal()
    save_requested = Signal()
    load_requested = Signal()
    toggle_view_requested = Signal()
    next_page_requested = Signal()
    prev_page_requested = Signal()
    first_page_requested = Signal()
    last_page_requested = Signal()
    per_page_changed = Signal(int)
    close_connection = Signal()

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._add_icons()
        self._connect_signals()

    def _add_icons(self):
        ICON_SIZE = QSize(18, 18)
        PATH_TO_RESOURCES = "/Users/shoptick/Documents/BSUIR/sem4/PPOIS/L2/resources"

        buttons = {
            # self.ui.logoLabel:          PATH_TO_RESOURCES + "/images/logo.svg",
            self.ui.btnAdd:             PATH_TO_RESOURCES + "/images/plus.svg",
            self.ui.btnSearch:          PATH_TO_RESOURCES + "/images/search.svg",
            self.ui.btnDeleteSidebar:   PATH_TO_RESOURCES + "/images/trash.svg",
            self.ui.btnToggleTree:      PATH_TO_RESOURCES + "/images/table.svg",
            self.ui.btnLoad:            PATH_TO_RESOURCES + "/images/upload.svg",
            self.ui.btnSave:            PATH_TO_RESOURCES + "/images/download.svg",
        }

        for btn, path in buttons.items():
            btn.setIcon(QIcon(path))
            btn.setIconSize(ICON_SIZE)

        self.ui.logoLabel.setText("  ВетЖурнал")
        self.ui.btnAdd.setText("  Добавить")
        self.ui.btnSearch.setText("  Поиск")
        self.ui.btnDeleteSidebar.setText("  Удалить")
        self.ui.btnToggleTree.setText("  Вид: таблица")
        self.ui.btnLoad.setText("  Загрузить")
        self.ui.btnSave.setText("  Сохранить")

    def _connect_signals(self):
        self.ui.btnAdd.clicked.connect(self.add_requested)
        self.ui.btnSearch.clicked.connect(self.search_requested)
        self.ui.btnDeleteSidebar.clicked.connect(self.delete_requested)
        self.ui.btnSave.clicked.connect(self.save_requested)
        self.ui.btnLoad.clicked.connect(self.load_requested)
        self.ui.btnToggleTree.clicked.connect(self.toggle_view_requested)
        self.ui.btnNextPage.clicked.connect(self.next_page_requested)
        self.ui.btnPrevPage.clicked.connect(self.prev_page_requested)
        self.ui.btnFirstPage.clicked.connect(self.first_page_requested)
        self.ui.btnLastPage.clicked.connect(self.last_page_requested)
        self.ui.perPageSpinBox.valueChanged.connect(self.per_page_changed)

    def set_table_model(self, model):
        self.ui.recordTable.setModel(model)

    def set_tree_data(self, records) -> None:
        tree = self.ui.recordTree
        tree.clear()
        fields = [
            ("Имя питомца",       lambda r: r.pet_name),
            ("Дата рождения",     lambda r: r.birth_date.strftime("%d.%m.%Y")),
            ("Дата посл. приёма", lambda r: r.last_visit_date.strftime("%d.%m.%Y")),
            ("ФИО ветеринара",    lambda r: r.vet_name),
            ("Диагноз",           lambda r: r.diagnosis),
        ]
        for i, record in enumerate(records, start=1):
            root = QTreeWidgetItem(tree, [f"Запись #{i}  —  {record.pet_name}", ""])
            for label, getter in fields:
                QTreeWidgetItem(root, [label, getter(record)])
        tree.expandAll()

    def switch_view(self, show_tree: bool) -> None:
        self.ui.contentStack.setCurrentIndex(1 if show_tree else 0)
        self.ui.btnToggleTree.setText("  Вид: дерево" if show_tree else "  Вид: таблица")

    def is_tree_view(self) -> bool:
        return self.ui.contentStack.currentIndex() == 1

    def update_pagination(self, current_page, total_pages, total_records):
        self.ui.pageLabel.setText("Стр.")
        self.ui.totalPagesLabel.setText(f"из {total_pages}")
        self.ui.totalRecordsLabel.setText(f"Всего записей: {total_records}")
        self.ui.currentPageSpinBox.setValue(current_page)

        on_first = current_page <= 1
        on_last = current_page >= total_pages
        self.ui.btnFirstPage.setEnabled(not on_first)
        self.ui.btnPrevPage.setEnabled(not on_first)
        self.ui.btnNextPage.setEnabled(not on_last)
        self.ui.btnLastPage.setEnabled(not on_last)

    def confirm(self, title: str, message: str) -> bool:
        answer = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        return answer == QMessageBox.Yes

    def notify(self, message: str, title: str = "Уведомление") -> None:
        QMessageBox.warning(self, title, message)

    def ask_save_path(self) -> Path | None:
        path_str, _ = QFileDialog.getSaveFileName(
            self, "Экспорт в XML", "", "XML (*.xml)"
        )
        if not path_str:
            return None
        path = Path(path_str)
        if not path.suffix:
            path = path.with_suffix(".xml")
        return path

    def ask_open_path(self) -> Path | None:
        path_str, _ = QFileDialog.getOpenFileName(
            self, "Импорт из XML", "", "XML (*.xml)"
        )
        return Path(path_str) if path_str else None

    def create_record_dialog(self, mode: DialogMode) -> RecordDialog:
        return RecordDialog(mode, parent=self)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close_connection.emit()