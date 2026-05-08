# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QSpinBox, QStackedWidget, QTableView,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)
from .resources_rc import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1225, 769)
        MainWindow.setMinimumSize(QSize(1100, 680))
        MainWindow.setMaximumSize(QSize(16777215, 16777215))
        font = QFont()
        font.setFamilies([u"Inter"])
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"/* \u2500\u2500 \u0413\u043b\u043e\u0431\u0430\u043b\u044c\u043d\u044b\u0439 \u0448\u0440\u0438\u0444\u0442 \u0438 \u0446\u0432\u0435\u0442 \u0442\u0435\u043a\u0441\u0442\u0430 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"* {\n"
"    font-family: \"Inter\";\n"
"	/* sans-serif*/\n"
"    font-size: 13px;\n"
"    color: #40513B;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0424\u043e\u043d \u043e\u043a\u043d\u0430 \u0438 \u0432\u0441\u0435\u0445 QWidget \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QMainWindow, QWidget {\n"
"    background-color: #EDF1D6;\n"
"}\n"
"\n"
"/* \u2500\u2500 MenuBar \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QMenuBar {\n"
"    background-color: #40513B;\n"
"    color: #fcfcfc;\n"
"    padding: 2px 4px;\n"
"    spacing: 4px;\n"
"}\n"
"QMenuBar::item {\n"
"    background: transparent;\n"
"    padding: 4px 12px;\n"
"    border-radius: 4px;\n"
"    color: #fcfcfc;\n"
"}\n"
"QMenuBar::item:selected {\n"
"    background-color: #609966;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0412\u044b\u043f\u0430\u0434\u0430\u044e\u0449\u0438\u0435 \u043c\u0435\u043d\u044e \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QMenu {\n"
"    background-color: #EDF1D6;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 6px;\n"
"    padding: 4px 0;\n"
"}\n"
"QMenu::item {\n"
"    padding: 6px 24px 6px 12px;\n"
"    border-radius: 4px"
                        ";\n"
"    margin: 1px 4px;\n"
"    color: #40513B;\n"
"}\n"
"QMenu::item:selected {\n"
"    background-color: #9DC08B;\n"
"    color: #40513B;\n"
"}\n"
"QMenu::separator {\n"
"    height: 1px;\n"
"    background: #9DC08B;\n"
"    margin: 4px 8px;\n"
"}\n"
"\n"
"/* \u2500\u2500 ToolBar \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QToolBar {\n"
"    background-color: #40513B;\n"
"    border: none;\n"
"    padding: 4px 6px;\n"
"    spacing: 4px;\n"
"}\n"
"QToolBar::separator {\n"
"    width: 1px;\n"
"    background: #609966;\n"
"    margin: 4px 4px;\n"
"}\n"
"QToolButton {\n"
"    background-color: transparent;\n"
"    color: #fcfcfc;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"    min-width: 32px;\n"
"    min-height: 32px;\n"
"}\n"
""
                        "QToolButton:hover   { background-color: #609966; }\n"
"QToolButton:pressed { background-color: #40513B; border: 1px solid #9DC08B; }\n"
"QToolButton:checked { background-color: #609966; border: 1px solid #9DC08B; }\n"
"\n"
"/* \u2500\u2500 Sidebar \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QFrame#sidebar {\n"
"    background-color: #40513B;\n"
"    border-right: 2px solid #609966;\n"
"}\n"
"\n"
"/* \u041b\u043e\u0433\u043e\u0442\u0438\u043f \u0432 \u0441\u0430\u0439\u0434\u0431\u0430\u0440\u0435 */\n"
"QLabel#logoLabel {\n"
"    color: #fcfcee;\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"    background-color: #40513B;\n"
"}\n"
"\n"
"/* \u0420\u0430\u0437\u0434\u0435\u043b\u0438\u0442\u0435\u043b\u0438 \u0432 \u0441\u0430\u0439\u0434\u0431\u0430\u0440"
                        "\u0435 */\n"
"QFrame#sidebarDivider,\n"
"QFrame#sidebarDivider2,\n"
"QFrame#sidebarDivider3 {\n"
"    background-color: #548046;\n"
"    border: none;\n"
"}\n"
"\n"
"/* \u0412\u0421\u0415 \u043a\u043d\u043e\u043f\u043a\u0438 \u0432\u043d\u0443\u0442\u0440\u0438 sidebar \u2014 \u0431\u0435\u0437 \u043f\u043e\u0432\u0442\u043e\u0440\u0435\u043d\u0438\u0439 \u043d\u0430 \u043a\u0430\u0436\u0434\u043e\u0439 \u043a\u043d\u043e\u043f\u043a\u0435 */\n"
"QFrame#sidebar QPushButton {\n"
"    background-color: transparent;\n"
"    color: #fcfcee;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    text-align: left;\n"
"    padding: 9px 14px;\n"
"    font-size: 13px;\n"
"    margin: 4px 2px 8px;\n"
"}\n"
"QFrame#sidebar QPushButton:hover   { background-color: #6DA65B; }\n"
"QFrame#sidebar QPushButton:pressed { background-color: #EDF1D6; color: #40513B; }\n"
"QFrame#sidebar QPushButton:checked { background-color: qlineargradient(\n"
"        x1: 0, y1: 0, x2: 1, y2: 0,\n"
"        stop: 0 #F8FCE0,      /* \u041d\u0430"
                        "\u0447\u0430\u043b\u043e \"\u0433\u0440\u0430\u043d\u0438\u0446\u044b\" */\n"
"        stop: 0.05 #F8FCE0,   /* \u041a\u043e\u043d\u0435\u0446 \"\u0433\u0440\u0430\u043d\u0438\u0446\u044b\" (3% \u0448\u0438\u0440\u0438\u043d\u044b) */\n"
"        stop: 0.05 #6DA65B,   /* \u0420\u0435\u0437\u043a\u0438\u0439 \u043f\u0435\u0440\u0435\u0445\u043e\u0434 \u0432 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0446\u0432\u0435\u0442 */\n"
"        stop: 1 #6DA65B       /* \u041e\u0441\u043d\u043e\u0432\u043d\u043e\u0439 \u0446\u0432\u0435\u0442 \u0434\u043e \u043a\u043e\u043d\u0446\u0430 \u043a\u043d\u043e\u043f\u043a\u0438 */\n"
"    ); \n"
"	font-weight: bold;\n"
"}\n"
"\n"
"/* \u041c\u0435\u0442\u043a\u0430 \u0438\u043c\u0435\u043d\u0438 \u0444\u0430\u0439\u043b\u0430 */\n"
"QLabel#configNameLabel {\n"
"    color: #9DC08B;\n"
"    font-size: 11px;\n"
"    padding: 4px 6px 0 6px;\n"
"    background-color: #40513B;\n"
"}\n"
"\n"
"/* \u2500\u2500 QTableView \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QTableView#recordTable {\n"
"    background-color: #F8FCE0;\n"
"    alternate-background-color: #F8FCE0;\n"
"    gridline-color: #C8D8B0;\n"
"    border: none;\n"
"    selection-background-color: #F8FCE0;\n"
"    selection-color: #40513B;\n"
"}\n"
"QTableView#recordTable::item {\n"
"    padding: 6px 10px;\n"
"    border-bottom: 1px solid #E0EAC8;\n"
"}\n"
"QTableView#recordTable::item:selected {\n"
"    background-color: #9DC08B;\n"
"    color: #40513B;\n"
"}\n"
"\n"
"/* \u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043a\u0438 \u0442\u0430\u0431\u043b\u0438\u0446\u044b \u0438 \u0434\u0435\u0440\u0435\u0432\u0430 */\n"
"QHeaderView::section {\n"
"    background-color: #40513B;\n"
"    color: #EDF1D6;\n"
"    padding: 8px 10px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    border-right: 1p"
                        "x solid #609966;\n"
"}\n"
"QHeaderView::section:hover { background-color: #609966; }\n"
"\n"
"/* \u2500\u2500 QTreeWidget \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QTreeWidget#recordTree {\n"
"    background-color: #F8FCE0;\n"
"    alternate-background-color: #F8FCE0;\n"
"    border: none;\n"
"    selection-background-color: #9DC08B;\n"
"    selection-color: #40513B;\n"
"}\n"
"QTreeWidget#recordTree::item {\n"
"    padding: 4px 6px;\n"
"    border-bottom: 1px solid #E0EAC8;\n"
"}\n"
"QTreeWidget#recordTree::item:selected { background-color: #9DC08B; color: #40513B; }\n"
"QTreeWidget#recordTree::branch { background: transparent; color: #40513B; }\n"
"QTreeWidget#recordTree::branch:has-children:!has-siblings:closed,\n"
"QTreeWidget#recordTree::branch:closed:has-children:has-siblings {\n"
""
                        "    image: url(:/resources/images/arrow_right.svg);\n"
"}\n"
"QTreeWidget#recordTree::branch:open:has-children:!has-siblings,\n"
"QTreeWidget#recordTree::branch:open:has-children:has-siblings {\n"
"    image: url(:/resources/images/arrow_down.svg);\n"
"}\n"
"\n"
"/* \u2500\u2500 Pagination Bar \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QFrame#paginationBar {\n"
"    background-color: #AAC78F;\n"
"    border-top: 1px solid #609966;\n"
"}\n"
"\n"
"/* \u041a\u043d\u043e\u043f\u043a\u0438 \u0432\u043d\u0443\u0442\u0440\u0438 paginationBar */\n"
"QFrame#paginationBar QPushButton {\n"
"    background-color: #6DA65B;\n"
"    color: #fcfcee;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    min-width: 28px; max-width: 28px;\n"
"    min-height: 26px; max-height: 26px;\n"
"    font-size: 14px;\n"
"    fon"
                        "t-weight: bold;\n"
"    padding: 0;\n"
"}\n"
"QFrame#paginationBar QPushButton:hover     { background-color: #40513B; }\n"
"QFrame#paginationBar QPushButton:disabled  { background-color: #C8D8B0; color: #9DC08B; }\n"
"\n"
"/* \u041c\u0435\u0442\u043a\u0438 \u0432\u043d\u0443\u0442\u0440\u0438 paginationBar */\n"
"QFrame#paginationBar QLabel {\n"
"    color: #40513B;\n"
"    font-size: 12px;\n"
"    padding: 0 4px;\n"
"    background-color: transparent;\n"
"}\n"
"QLabel#totalRecordsLabel { color: #5A6B52; }\n"
"\n"
"/* \u0422\u043e\u043d\u043a\u0438\u0435 \u0432\u0435\u0440\u0442\u0438\u043a\u0430\u043b\u044c\u043d\u044b\u0435 \u0440\u0430\u0437\u0434\u0435\u043b\u0438\u0442\u0435\u043b\u0438-\u0433\u0440\u0443\u043f\u043f\u044b \u0432\u043d\u0443\u0442\u0440\u0438 paginationBar */\n"
"QFrame#paginationSeparator1, QFrame#paginationSeparator2 {\n"
"    color: #7FA374;\n"
"    background-color: #7FA374;\n"
"}\n"
"\n"
"/* SpinBox \u0432\u043d\u0443\u0442\u0440\u0438 paginationBar */\n"
"\n"
"QFrame#paginationBar Q"
                        "SpinBox {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #609966;\n"
"    border-radius: 4px;\n"
"    padding: 2px 4px;\n"
"    color: #40513B;\n"
"    min-height: 24px; max-height: 24px;\n"
"    font-size: 12px;\n"
"}\n"
"QFrame#paginationBar QSpinBox::up-button,\n"
"QFrame#paginationBar QSpinBox::down-button {\n"
"    width: 16px;\n"
"    background: #609966;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u041f\u043e\u043b\u044f \u0432\u0432\u043e\u0434\u0430 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QLineEdit, QTextEdit, QPlainTextEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 6px 8px;\n"
"    color: #40513B;\n"
"    selection-background-color: #9DC08B;\n"
"}\n"
"QLineEdit:focus, QTextEdit:focus { borde"
                        "r: 1.5px solid #609966; background-color: #F8FAF0; }\n"
"QLineEdit:disabled               { background-color: #F0F3E4; color: #9DC08B; }\n"
"\n"
"/* \u2500\u2500 DateEdit \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QDateEdit, QDateTimeEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 5px 8px;\n"
"    color: #40513B;\n"
"    min-height: 28px;\n"
"}\n"
"QDateEdit:focus, QDateTimeEdit:focus { border: 1.5px solid #609966; }\n"
"QDateEdit::drop-down, QDateTimeEdit::drop-down { border: none; width: 20px; }\n"
"\n"
"QCalendarWidget { background-color: #EDF1D6; border: 1px solid #9DC08B; border-radius: 6px; }\n"
"QCalendarWidget QToolButton { background-color: #40513B; color: #EDF1D6; border-radius: 4px; p"
                        "adding: 4px; }\n"
"QCalendarWidget QAbstractItemView { background-color: #ffffff; selection-background-color: #9DC08B; selection-color: #40513B; }\n"
"\n"
"/* \u2500\u2500 SpinBox \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QSpinBox, QDoubleSpinBox {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 5px 8px;\n"
"    color: #40513B;\n"
"    min-height: 28px;\n"
"}\n"
"QSpinBox:focus, QDoubleSpinBox:focus { border: 1.5px solid #609966; }\n"
"\n"
"QFrame#paginationBar QSpinBox::up-arrow {\n"
"    image: url(:/resources/images/up_arrow.svg);\n"
"    width: 8px;\n"
"    height: 5px;\n"
"}\n"
"\n"
"QFrame#paginationBar QSpinBox::down-arrow {\n"
"    image: url(:/resources/images/down_arrow.svg);\n"
"    w"
                        "idth: 8px;\n"
"    height: 5px;\n"
"}\n"
"\n"
"/* \u2500\u2500 ComboBox \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QComboBox {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 5px 10px;\n"
"    color: #40513B;\n"
"    min-height: 28px;\n"
"}\n"
"QComboBox:focus            { border: 1.5px solid #609966; }\n"
"QComboBox::drop-down       { border: none; width: 22px; }\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #EDF1D6;\n"
"    border: 1px solid #9DC08B;\n"
"    selection-background-color: #9DC08B;\n"
"    selection-color: #40513B;\n"
"}\n"
"\n"
"/* \u2500\u2500 CheckBox \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QCheckBox { color: #40513B; spacing: 8px; }\n"
"QCheckBox::indicator {\n"
"    width: 16px; height: 16px;\n"
"    border: 1.5px solid #609966;\n"
"    border-radius: 3px;\n"
"    background-color: #ffffff;\n"
"}\n"
"QCheckBox::indicator:checked { background-color: #609966; border-color: #609966; }\n"
"QCheckBox::indicator:hover   { border-color: #40513B; }\n"
"\n"
"/* \u2500\u2500 \u0421\u043a\u0440\u043e\u043b\u043b\u0431\u0430\u0440\u044b \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QScrollBar:vertical   { background: #EDF1D6; width: 8px;  border-radius: 4px; margin: 0; }\n"
"QScrollBar:horizontal { background: #EDF1D6"
                        "; height: 8px; border-radius: 4px; margin: 0; }\n"
"QScrollBar::handle:vertical   { background: #9DC08B; border-radius: 4px; min-height: 30px; }\n"
"QScrollBar::handle:horizontal { background: #9DC08B; border-radius: 4px; min-width: 30px; }\n"
"QScrollBar::handle:vertical:hover,\n"
"QScrollBar::handle:horizontal:hover { background: #609966; }\n"
"QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical,\n"
"QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { height: 0; width: 0; background: none; }\n"
"\n"
"/* \u2500\u2500 StatusBar \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QStatusBar {\n"
"    background-color: #40513B;\n"
"    color: #9DC08B;\n"
"    font-size: 11px;\n"
"    padding: 2px 8px;\n"
"}\n"
"QStatusBar::item { border: none; }\n"
"\n"
"/* \u2500"
                        "\u2500 ToolTip \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QToolTip {\n"
"    background-color: #40513B;\n"
"    color: #EDF1D6;\n"
"    border: 1px solid #609966;\n"
"    border-radius: 4px;\n"
"    padding: 4px 8px;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"/* \u2500\u2500 GroupBox (\u0434\u043b\u044f \u0434\u0438\u0430\u043b\u043e\u0433\u043e\u0432) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QGroupBox {\n"
"    border: 1.5px solid #9DC08B;\n"
"    border-radius: 6px;\n"
"    margin-top: 14px;\n"
"    padding: 8px 6px 6px 6px;\n"
"    color: #609966;\n"
"}\n"
"QGroupBox::title {\n"
"    subcontrol-origin: mar"
                        "gin;\n"
"    subcontrol-position: top left;\n"
"    padding: 0 6px;\n"
"    color: #609966;\n"
"    font-weight: bold;\n"
"}\n"
"   \n"
"/* --- TableView --- */\n"
"QTableWidget {\n"
"	background-color: #EDF1D6;\n"
"}\n"
"\n"
"QMessageBox {\n"
"    background-color: #EDF1D6;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 8px;\n"
"}\n"
"\n"
"QMessageBox QLabel {\n"
"    color: #40513B;\n"
"    font-size: 13px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"QMessageBox QPushButton {\n"
"    background-color: #609966;\n"
"    color: #fcfcee;\n"
"    border: none;\n"
"    border-radius: 5px;\n"
"    padding: 6px 20px;\n"
"    font-size: 13px;\n"
"    min-width: 72px;\n"
"    min-height: 28px;\n"
"}\n"
"\n"
"QMessageBox QPushButton:hover {\n"
"    background-color: #40513B;\n"
"}\n"
"\n"
"QMessageBox QPushButton:pressed {\n"
"    background-color: #2e3d2a;\n"
"    border: 1px solid #9DC08B;\n"
"}\n"
"\n"
"QMessageBox QPushButton:default {\n"
"    border: 2px solid #40513B;\n"
"}")
        self.actionSaveToFile = QAction(MainWindow)
        self.actionSaveToFile.setObjectName(u"actionSaveToFile")
        self.actionLoadFromFile = QAction(MainWindow)
        self.actionLoadFromFile.setObjectName(u"actionLoadFromFile")
        self.actionSaveToDb = QAction(MainWindow)
        self.actionSaveToDb.setObjectName(u"actionSaveToDb")
        self.actionLoadFromDb = QAction(MainWindow)
        self.actionLoadFromDb.setObjectName(u"actionLoadFromDb")
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAdd = QAction(MainWindow)
        self.actionAdd.setObjectName(u"actionAdd")
        self.actionSearch = QAction(MainWindow)
        self.actionSearch.setObjectName(u"actionSearch")
        self.actionDelete = QAction(MainWindow)
        self.actionDelete.setObjectName(u"actionDelete")
        self.actionToggleTree = QAction(MainWindow)
        self.actionToggleTree.setObjectName(u"actionToggleTree")
        self.actionToggleTree.setCheckable(True)
        self.actionToggleTree.setChecked(False)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName(u"actionSettings")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.mainHLayout = QHBoxLayout(self.centralwidget)
        self.mainHLayout.setSpacing(0)
        self.mainHLayout.setObjectName(u"mainHLayout")
        self.mainHLayout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QFrame(self.centralwidget)
        self.sidebar.setObjectName(u"sidebar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar.sizePolicy().hasHeightForWidth())
        self.sidebar.setSizePolicy(sizePolicy)
        self.sidebar.setMinimumSize(QSize(200, 0))
        self.sidebar.setMaximumSize(QSize(200, 16777215))
        self.sidebar.setFrameShape(QFrame.Shape.StyledPanel)
        self.sidebar.setFrameShadow(QFrame.Shadow.Plain)
        self.sidebar.setLineWidth(1)
        self.sidebarLayout = QVBoxLayout(self.sidebar)
        self.sidebarLayout.setSpacing(4)
        self.sidebarLayout.setObjectName(u"sidebarLayout")
        self.sidebarLayout.setContentsMargins(8, 0, 8, 8)
        self.logoLabel = QLabel(self.sidebar)
        self.logoLabel.setObjectName(u"logoLabel")
        self.logoLabel.setMinimumSize(QSize(0, 70))
        self.logoLabel.setMaximumSize(QSize(16777215, 70))
        self.logoLabel.setStyleSheet(u"")
        self.logoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sidebarLayout.addWidget(self.logoLabel)

        self.sidebarDivider = QFrame(self.sidebar)
        self.sidebarDivider.setObjectName(u"sidebarDivider")
        self.sidebarDivider.setMinimumSize(QSize(0, 1))
        self.sidebarDivider.setMaximumSize(QSize(16777215, 1))
        self.sidebarDivider.setFrameShape(QFrame.Shape.HLine)
        self.sidebarDivider.setFrameShadow(QFrame.Shadow.Plain)

        self.sidebarLayout.addWidget(self.sidebarDivider)

        self.btnAdd = QPushButton(self.sidebar)
        self.btnAdd.setObjectName(u"btnAdd")
        self.btnAdd.setMinimumSize(QSize(0, 0))
        self.btnAdd.setMaximumSize(QSize(16777215, 16777215))
        self.btnAdd.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.btnAdd)

        self.btnSearch = QPushButton(self.sidebar)
        self.btnSearch.setObjectName(u"btnSearch")
        self.btnSearch.setMinimumSize(QSize(0, 0))
        self.btnSearch.setMaximumSize(QSize(16777215, 16777215))
        self.btnSearch.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.btnSearch)

        self.btnDeleteSidebar = QPushButton(self.sidebar)
        self.btnDeleteSidebar.setObjectName(u"btnDeleteSidebar")
        self.btnDeleteSidebar.setMinimumSize(QSize(0, 0))
        self.btnDeleteSidebar.setMaximumSize(QSize(16777215, 16777215))
        self.btnDeleteSidebar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.btnDeleteSidebar)

        self.btnToggleTree = QPushButton(self.sidebar)
        self.btnToggleTree.setObjectName(u"btnToggleTree")
        self.btnToggleTree.setMinimumSize(QSize(0, 0))
        self.btnToggleTree.setMaximumSize(QSize(16777215, 16777215))
        self.btnToggleTree.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btnToggleTree.setCheckable(True)
        self.btnToggleTree.setChecked(False)

        self.sidebarLayout.addWidget(self.btnToggleTree)

        self.sidebarVSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.sidebarLayout.addItem(self.sidebarVSpacer)

        self.sidebarDivider2 = QFrame(self.sidebar)
        self.sidebarDivider2.setObjectName(u"sidebarDivider2")
        self.sidebarDivider2.setMinimumSize(QSize(0, 1))
        self.sidebarDivider2.setMaximumSize(QSize(16777215, 1))
        self.sidebarDivider2.setFrameShape(QFrame.Shape.HLine)
        self.sidebarDivider2.setFrameShadow(QFrame.Shadow.Plain)

        self.sidebarLayout.addWidget(self.sidebarDivider2)

        self.btnSave = QPushButton(self.sidebar)
        self.btnSave.setObjectName(u"btnSave")
        self.btnSave.setMinimumSize(QSize(0, 0))
        self.btnSave.setMaximumSize(QSize(16777215, 16777215))
        self.btnSave.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.btnSave)

        self.btnLoad = QPushButton(self.sidebar)
        self.btnLoad.setObjectName(u"btnLoad")
        self.btnLoad.setMinimumSize(QSize(0, 0))
        self.btnLoad.setMaximumSize(QSize(16777215, 16777215))
        self.btnLoad.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sidebarLayout.addWidget(self.btnLoad)


        self.mainHLayout.addWidget(self.sidebar)

        self.contentArea = QFrame(self.centralwidget)
        self.contentArea.setObjectName(u"contentArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.contentArea.sizePolicy().hasHeightForWidth())
        self.contentArea.setSizePolicy(sizePolicy1)
        self.contentArea.setFrameShape(QFrame.Shape.NoFrame)
        self.contentArea.setFrameShadow(QFrame.Shadow.Plain)
        self.contentLayout = QVBoxLayout(self.contentArea)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setObjectName(u"contentLayout")
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentStack = QStackedWidget(self.contentArea)
        self.contentStack.setObjectName(u"contentStack")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.contentStack.sizePolicy().hasHeightForWidth())
        self.contentStack.setSizePolicy(sizePolicy2)
        self.pageTable = QWidget()
        self.pageTable.setObjectName(u"pageTable")
        self.pageTableLayout = QVBoxLayout(self.pageTable)
        self.pageTableLayout.setSpacing(0)
        self.pageTableLayout.setObjectName(u"pageTableLayout")
        self.pageTableLayout.setContentsMargins(0, 0, 0, 0)
        self.recordTable = QTableView(self.pageTable)
        self.recordTable.setObjectName(u"recordTable")
        sizePolicy2.setHeightForWidth(self.recordTable.sizePolicy().hasHeightForWidth())
        self.recordTable.setSizePolicy(sizePolicy2)
        self.recordTable.setAutoFillBackground(True)
        self.recordTable.setStyleSheet(u"background-color:#F8FCE0;")
        self.recordTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.recordTable.setAlternatingRowColors(True)
        self.recordTable.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.recordTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.recordTable.setShowGrid(True)
        self.recordTable.setGridStyle(Qt.PenStyle.SolidLine)
        self.recordTable.setSortingEnabled(True)
        self.recordTable.horizontalHeader().setMinimumSectionSize(60)
        self.recordTable.horizontalHeader().setDefaultSectionSize(140)
        self.recordTable.horizontalHeader().setStretchLastSection(True)
        self.recordTable.verticalHeader().setVisible(False)
        self.recordTable.verticalHeader().setDefaultSectionSize(32)

        self.pageTableLayout.addWidget(self.recordTable)

        self.contentStack.addWidget(self.pageTable)
        self.pageTree = QWidget()
        self.pageTree.setObjectName(u"pageTree")
        self.pageTree.setEnabled(True)
        self.pageTreeLayout = QVBoxLayout(self.pageTree)
        self.pageTreeLayout.setSpacing(0)
        self.pageTreeLayout.setObjectName(u"pageTreeLayout")
        self.pageTreeLayout.setContentsMargins(0, 0, 0, 0)
        self.recordTree = QTreeWidget(self.pageTree)
        self.recordTree.setObjectName(u"recordTree")
        sizePolicy2.setHeightForWidth(self.recordTree.sizePolicy().hasHeightForWidth())
        self.recordTree.setSizePolicy(sizePolicy2)
        self.recordTree.setAlternatingRowColors(True)
        self.recordTree.setIndentation(20)
        self.recordTree.setUniformRowHeights(True)
        self.recordTree.setSortingEnabled(True)
        self.recordTree.header().setStretchLastSection(True)

        self.pageTreeLayout.addWidget(self.recordTree)

        self.contentStack.addWidget(self.pageTree)

        self.contentLayout.addWidget(self.contentStack)

        self.paginationBar = QFrame(self.contentArea)
        self.paginationBar.setObjectName(u"paginationBar")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.paginationBar.sizePolicy().hasHeightForWidth())
        self.paginationBar.setSizePolicy(sizePolicy3)
        self.paginationBar.setMinimumSize(QSize(0, 42))
        self.paginationBar.setMaximumSize(QSize(16777215, 42))
        self.paginationBar.setFrameShape(QFrame.Shape.StyledPanel)
        self.paginationBar.setFrameShadow(QFrame.Shadow.Plain)
        self.paginationLayout = QHBoxLayout(self.paginationBar)
        self.paginationLayout.setSpacing(8)
        self.paginationLayout.setObjectName(u"paginationLayout")
        self.paginationLayout.setContentsMargins(14, 0, 14, 0)
        self.totalRecordsLabel = QLabel(self.paginationBar)
        self.totalRecordsLabel.setObjectName(u"totalRecordsLabel")
        self.totalRecordsLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.paginationLayout.addWidget(self.totalRecordsLabel)

        self.paginationSpacerLeft = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationLayout.addItem(self.paginationSpacerLeft)

        self.paginationSeparator1 = QFrame(self.paginationBar)
        self.paginationSeparator1.setObjectName(u"paginationSeparator1")
        self.paginationSeparator1.setMinimumSize(QSize(1, 22))
        self.paginationSeparator1.setMaximumSize(QSize(1, 22))
        self.paginationSeparator1.setFrameShape(QFrame.Shape.VLine)
        self.paginationSeparator1.setFrameShadow(QFrame.Shadow.Plain)

        self.paginationLayout.addWidget(self.paginationSeparator1)

        self.btnFirstPage = QPushButton(self.paginationBar)
        self.btnFirstPage.setObjectName(u"btnFirstPage")
        self.btnFirstPage.setMinimumSize(QSize(28, 26))
        self.btnFirstPage.setMaximumSize(QSize(28, 26))
        self.btnFirstPage.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnFirstPage)

        self.btnPrevPage = QPushButton(self.paginationBar)
        self.btnPrevPage.setObjectName(u"btnPrevPage")
        self.btnPrevPage.setMinimumSize(QSize(28, 26))
        self.btnPrevPage.setMaximumSize(QSize(28, 26))
        self.btnPrevPage.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnPrevPage)

        self.pageLabel = QLabel(self.paginationBar)
        self.pageLabel.setObjectName(u"pageLabel")
        self.pageLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.paginationLayout.addWidget(self.pageLabel)

        self.currentPageSpinBox = QSpinBox(self.paginationBar)
        self.currentPageSpinBox.setObjectName(u"currentPageSpinBox")
        self.currentPageSpinBox.setMinimumSize(QSize(55, 30))
        self.currentPageSpinBox.setMaximumSize(QSize(55, 30))
        self.currentPageSpinBox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.currentPageSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.currentPageSpinBox.setMinimum(1)
        self.currentPageSpinBox.setMaximum(9999)
        self.currentPageSpinBox.setValue(1)

        self.paginationLayout.addWidget(self.currentPageSpinBox)

        self.totalPagesLabel = QLabel(self.paginationBar)
        self.totalPagesLabel.setObjectName(u"totalPagesLabel")
        self.totalPagesLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.paginationLayout.addWidget(self.totalPagesLabel)

        self.btnNextPage = QPushButton(self.paginationBar)
        self.btnNextPage.setObjectName(u"btnNextPage")
        self.btnNextPage.setMinimumSize(QSize(28, 26))
        self.btnNextPage.setMaximumSize(QSize(28, 26))
        self.btnNextPage.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnNextPage)

        self.btnLastPage = QPushButton(self.paginationBar)
        self.btnLastPage.setObjectName(u"btnLastPage")
        self.btnLastPage.setMinimumSize(QSize(28, 26))
        self.btnLastPage.setMaximumSize(QSize(28, 26))
        self.btnLastPage.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnLastPage)

        self.paginationSeparator2 = QFrame(self.paginationBar)
        self.paginationSeparator2.setObjectName(u"paginationSeparator2")
        self.paginationSeparator2.setMinimumSize(QSize(1, 22))
        self.paginationSeparator2.setMaximumSize(QSize(1, 22))
        self.paginationSeparator2.setFrameShape(QFrame.Shape.VLine)
        self.paginationSeparator2.setFrameShadow(QFrame.Shadow.Plain)

        self.paginationLayout.addWidget(self.paginationSeparator2)

        self.paginationSpacerRight = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationLayout.addItem(self.paginationSpacerRight)

        self.perPageLabel = QLabel(self.paginationBar)
        self.perPageLabel.setObjectName(u"perPageLabel")
        self.perPageLabel.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.paginationLayout.addWidget(self.perPageLabel)

        self.perPageSpinBox = QSpinBox(self.paginationBar)
        self.perPageSpinBox.setObjectName(u"perPageSpinBox")
        self.perPageSpinBox.setMinimumSize(QSize(58, 30))
        self.perPageSpinBox.setMaximumSize(QSize(58, 30))
        self.perPageSpinBox.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.perPageSpinBox.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.perPageSpinBox.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.perPageSpinBox.setMinimum(5)
        self.perPageSpinBox.setMaximum(100)
        self.perPageSpinBox.setSingleStep(5)
        self.perPageSpinBox.setValue(10)

        self.paginationLayout.addWidget(self.perPageSpinBox)


        self.contentLayout.addWidget(self.paginationBar)


        self.mainHLayout.addWidget(self.contentArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QMenuBar(MainWindow)
        self.menuBar.setObjectName(u"menuBar")
        self.menuBar.setGeometry(QRect(0, 0, 1225, 29))
        self.menuFile = QMenu(self.menuBar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuRecords = QMenu(self.menuBar)
        self.menuRecords.setObjectName(u"menuRecords")
        self.menuView = QMenu(self.menuBar)
        self.menuView.setObjectName(u"menuView")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName(u"menuHelp")
        MainWindow.setMenuBar(self.menuBar)
        QWidget.setTabOrder(self.btnAdd, self.btnSearch)
        QWidget.setTabOrder(self.btnSearch, self.btnDeleteSidebar)
        QWidget.setTabOrder(self.btnDeleteSidebar, self.btnToggleTree)
        QWidget.setTabOrder(self.btnToggleTree, self.btnSave)
        QWidget.setTabOrder(self.btnSave, self.btnLoad)
        QWidget.setTabOrder(self.btnLoad, self.recordTable)
        QWidget.setTabOrder(self.recordTable, self.recordTree)
        QWidget.setTabOrder(self.recordTree, self.btnFirstPage)
        QWidget.setTabOrder(self.btnFirstPage, self.btnPrevPage)
        QWidget.setTabOrder(self.btnPrevPage, self.currentPageSpinBox)
        QWidget.setTabOrder(self.currentPageSpinBox, self.perPageSpinBox)
        QWidget.setTabOrder(self.perPageSpinBox, self.btnNextPage)
        QWidget.setTabOrder(self.btnNextPage, self.btnLastPage)

        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuRecords.menuAction())
        self.menuBar.addAction(self.menuView.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionSaveToFile)
        self.menuFile.addAction(self.actionLoadFromFile)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveToDb)
        self.menuFile.addAction(self.actionLoadFromDb)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuRecords.addAction(self.actionAdd)
        self.menuRecords.addAction(self.actionSearch)
        self.menuRecords.addAction(self.actionDelete)
        self.menuView.addAction(self.actionToggleTree)
        self.menuHelp.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        self.contentStack.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0442\u0435\u0440\u0438\u043d\u0430\u0440\u043d\u044b\u0439 \u0436\u0443\u0440\u043d\u0430\u043b", None))
        self.actionSaveToFile.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 \u0444\u0430\u0439\u043b", None))
#if QT_CONFIG(tooltip)
        self.actionSaveToFile.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u0432 XML \u0444\u0430\u0439\u043b", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSaveToFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.actionLoadFromFile.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0438\u0437 \u0444\u0430\u0439\u043b\u0430", None))
#if QT_CONFIG(tooltip)
        self.actionLoadFromFile.setToolTip(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u0438\u0437 XML \u0444\u0430\u0439\u043b\u0430", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionLoadFromFile.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.actionSaveToDb.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0432 \u0411\u0414", None))
#if QT_CONFIG(tooltip)
        self.actionSaveToDb.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u0432 \u0431\u0430\u0437\u0443 \u0434\u0430\u043d\u043d\u044b\u0445 PostgreSQL", None))
#endif // QT_CONFIG(tooltip)
        self.actionLoadFromDb.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0438\u0437 \u0411\u0414", None))
#if QT_CONFIG(tooltip)
        self.actionLoadFromDb.setToolTip(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u0438\u0437 \u0431\u0430\u0437\u044b \u0434\u0430\u043d\u043d\u044b\u0445 PostgreSQL", None))
#endif // QT_CONFIG(tooltip)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0445\u043e\u0434", None))
#if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+Q", None))
#endif // QT_CONFIG(shortcut)
        self.actionAdd.setText(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.actionAdd.setToolTip(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u043e\u0432\u0443\u044e \u0437\u0430\u043f\u0438\u0441\u044c (Ctrl+N)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionAdd.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+N", None))
#endif // QT_CONFIG(shortcut)
        self.actionSearch.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
#if QT_CONFIG(tooltip)
        self.actionSearch.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u0437\u0430\u043f\u0438\u0441\u0435\u0439 (Ctrl+F)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionSearch.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+F", None))
#endif // QT_CONFIG(shortcut)
        self.actionDelete.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.actionDelete.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u043f\u043e \u0443\u0441\u043b\u043e\u0432\u0438\u044e", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actionDelete.setShortcut(QCoreApplication.translate("MainWindow", u"Del", None))
#endif // QT_CONFIG(shortcut)
        self.actionToggleTree.setText(QCoreApplication.translate("MainWindow", u"\u0414\u0435\u0440\u0435\u0432\u043e", None))
#if QT_CONFIG(tooltip)
        self.actionToggleTree.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0432\u0438\u0434: \u0442\u0430\u0431\u043b\u0438\u0446\u0430 / \u0434\u0435\u0440\u0435\u0432\u043e", None))
#endif // QT_CONFIG(tooltip)
        self.actionSettings.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438", None))
#if QT_CONFIG(tooltip)
        self.actionSettings.setToolTip(QCoreApplication.translate("MainWindow", u"\u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f", None))
#endif // QT_CONFIG(tooltip)
        self.logoLabel.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0435\u0442\u0416\u0443\u0440\u043d\u0430\u043b", None))
#if QT_CONFIG(tooltip)
        self.btnAdd.setToolTip(QCoreApplication.translate("MainWindow", u"\u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c \u043d\u043e\u0432\u0443\u044e \u0437\u0430\u043f\u0438\u0441\u044c (Ctrl+N)", None))
#endif // QT_CONFIG(tooltip)
        self.btnAdd.setText(QCoreApplication.translate("MainWindow", u"\uff0b  \u0414\u043e\u0431\u0430\u0432\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.btnSearch.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a \u0437\u0430\u043f\u0438\u0441\u0435\u0439 (Ctrl+F)", None))
#endif // QT_CONFIG(tooltip)
        self.btnSearch.setText(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0438\u0441\u043a", None))
#if QT_CONFIG(tooltip)
        self.btnDeleteSidebar.setToolTip(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u043f\u043e \u0443\u0441\u043b\u043e\u0432\u0438\u044e (Del)", None))
#endif // QT_CONFIG(tooltip)
        self.btnDeleteSidebar.setText(QCoreApplication.translate("MainWindow", u"\u0423\u0434\u0430\u043b\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.btnToggleTree.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0432\u0438\u0434 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u044f", None))
#endif // QT_CONFIG(tooltip)
        self.btnToggleTree.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434: \u0442\u0430\u0431\u043b\u0438\u0446\u0430", None))
#if QT_CONFIG(tooltip)
        self.btnSave.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u0432 XML \u0444\u0430\u0439\u043b", None))
#endif // QT_CONFIG(tooltip)
        self.btnSave.setText(QCoreApplication.translate("MainWindow", u"\u0421\u043e\u0445\u0440\u0430\u043d\u0438\u0442\u044c", None))
#if QT_CONFIG(tooltip)
        self.btnLoad.setToolTip(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0437\u0430\u043f\u0438\u0441\u0438 \u0438\u0437 XML \u0444\u0430\u0439\u043b\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnLoad.setText(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u0433\u0440\u0443\u0437\u0438\u0442\u044c", None))
        ___qtreewidgetitem = self.recordTree.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("MainWindow", u"\u0417\u043d\u0430\u0447\u0435\u043d\u0438\u0435", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0438\u0441\u044c / \u041f\u043e\u043b\u0435", None))
        self.totalRecordsLabel.setText(QCoreApplication.translate("MainWindow", u"\u0412\u0441\u0435\u0433\u043e \u0437\u0430\u043f\u0438\u0441\u0435\u0439: 0", None))
#if QT_CONFIG(tooltip)
        self.btnFirstPage.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0432\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnFirstPage.setText(QCoreApplication.translate("MainWindow", u"\u23ee", None))
#if QT_CONFIG(tooltip)
        self.btnPrevPage.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnPrevPage.setText(QCoreApplication.translate("MainWindow", u"\u25c0", None))
        self.pageLabel.setText(QCoreApplication.translate("MainWindow", u"\u0421\u0442\u0440.", None))
#if QT_CONFIG(tooltip)
        self.currentPageSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u0435\u0440\u0435\u0439\u0442\u0438 \u043a \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.totalPagesLabel.setText(QCoreApplication.translate("MainWindow", u"/ 1", None))
#if QT_CONFIG(tooltip)
        self.btnNextPage.setToolTip(QCoreApplication.translate("MainWindow", u"\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnNextPage.setText(QCoreApplication.translate("MainWindow", u"\u25b6", None))
#if QT_CONFIG(tooltip)
        self.btnLastPage.setToolTip(QCoreApplication.translate("MainWindow", u"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnLastPage.setText(QCoreApplication.translate("MainWindow", u"\u23ed", None))
        self.perPageLabel.setText(QCoreApplication.translate("MainWindow", u"\u041d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435:", None))
#if QT_CONFIG(tooltip)
        self.perPageSpinBox.setToolTip(QCoreApplication.translate("MainWindow", u"\u0427\u0438\u0441\u043b\u043e \u0437\u0430\u043f\u0438\u0441\u0435\u0439 \u043d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435", None))
#endif // QT_CONFIG(tooltip)
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"\u0424\u0430\u0439\u043b", None))
        self.menuRecords.setTitle(QCoreApplication.translate("MainWindow", u"\u0417\u0430\u043f\u0438\u0441\u0438", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"\u0412\u0438\u0434", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"\u0421\u043f\u0440\u0430\u0432\u043a\u0430", None))
    # retranslateUi

