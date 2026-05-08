import sys
from PySide6.QtWidgets import QApplication

from .view.main_window import MainWindow
from .controller.main_controller import MainController
from .model.db_manager import DBManager
from .model.xml_handler import XmlHandler


def main():
    app = QApplication(sys.argv)

    db = DBManager(
        host="localhost",
        port=5432,
        dbname="vetjournal",
        user="shoptick",
        password="",
    )
    xml = XmlHandler()

    window = MainWindow()
    controller = MainController(window, db, xml)

    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
