from math import ceil

from src.model.db_manager import DBManager
from src.model.xml_handler import XmlHandler
from src.view.main_window import MainWindow
from src.view.pet_table_model import PetTableModel
from src.view.record_dialog import DialogMode


class MainController:
    def __init__(self, window: MainWindow, db: DBManager, xml: XmlHandler) -> None:
        self._window = window
        self._db = db
        self._xml = xml
        self._current_page = 1
        self._per_page = 10

        window.add_requested.connect(self._on_add)
        window.search_requested.connect(self._on_search)
        window.delete_requested.connect(self._on_delete)
        window.toggle_view_requested.connect(self._on_toggle_view)
        window.save_requested.connect(self._on_save_xml)
        window.load_requested.connect(self._on_load_xml)
        window.next_page_requested.connect(self._on_next_page)
        window.prev_page_requested.connect(self._on_prev_page)
        window.first_page_requested.connect(self._on_first_page)
        window.last_page_requested.connect(self._on_last_page)
        window.per_page_changed.connect(self._on_per_page_changed)
        window.close_connection.connect(self._close_application)

        self._db.data_changed.connect(self._refresh)
        self._refresh()

    def _refresh(self) -> None:
        total = self._db.get_total_count()
        total_pages = max(1, ceil(total / self._per_page))
        self._current_page = max(1, min(self._current_page, total_pages))

        page_records = self._db.get_page(self._current_page, self._per_page)
        if self._window.is_tree_view():
            self._window.set_tree_data(page_records)
        else:
            self._window.set_table_model(PetTableModel(page_records))
        self._window.update_pagination(
            current_page=self._current_page,
            total_pages=total_pages,
            total_records=total,
        )

    def _on_toggle_view(self) -> None:
        show_tree = not self._window.is_tree_view()
        self._window.switch_view(show_tree)
        self._refresh()

    def _on_add(self) -> None:
        dlg = self._window.create_record_dialog(DialogMode.ADD)
        if dlg.exec():
            self._db.add(dlg.get_record())

    def _on_delete(self) -> None:
        dlg = self._window.create_record_dialog(DialogMode.DELETE)
        while dlg.exec():
            criteria = dlg.get_criteria()
            count = self._db.count_matching(criteria)
            if count == 0:
                self._window.notify("Нет записей, подходящих под критерии.")
                dlg.show_results([])
                continue
            if self._window.confirm("Подтверждение удаления", f"Будет удалено записей: {count}. Продолжить?"):
                self._db.delete_matching(criteria)
                return

    def _on_search(self) -> None:
        dlg = self._window.create_record_dialog(DialogMode.SEARCH)
        while dlg.exec():
            results = self._db.search(dlg.get_criteria())
            dlg.show_results(results)

    def _on_save_xml(self) -> None:
        path = self._window.ask_save_path()
        if path is None:
            return
        try:
            self._xml.export(self._db.get_all(), path)
        except Exception as e:
            self._window.notify(f"Ошибка при экспорте:\n{e}", "Ошибка")

    def _on_load_xml(self) -> None:
        if not self._window.confirm("Импорт", "Текущие данные будут заменены. Продолжить?"):
            return
        path = self._window.ask_open_path()
        if path is None:
            return
        try:
            records = self._xml.import_(path)
        except Exception as e:
            self._window.notify(f"Ошибка при импорте:\n{e}", "Ошибка")
            return
        self._db.replace_all(records)

    def _on_next_page(self) -> None:
        self._current_page = min(
            self._current_page + 1,
            max(1, ceil(self._db.get_total_count() / self._per_page)),
        )
        self._refresh()

    def _on_prev_page(self) -> None:
        self._current_page = max(self._current_page - 1, 1)
        self._refresh()

    def _on_first_page(self) -> None:
        self._current_page = 1
        self._refresh()

    def _on_last_page(self) -> None:
        self._current_page = max(1, ceil(self._db.get_total_count() / self._per_page))
        self._refresh()

    def _on_per_page_changed(self, value: int) -> None:
        self._per_page = value
        self._current_page = 1
        self._refresh()

    def _close_application(self) -> None:
        self._db.close()
