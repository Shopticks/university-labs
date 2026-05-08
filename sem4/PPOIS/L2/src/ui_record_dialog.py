# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'record_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QAbstractSpinBox, QApplication, QComboBox,
    QDateEdit, QDialog, QFormLayout, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTableView, QVBoxLayout, QWidget)

class Ui_RecordDialog(object):
    def setupUi(self, RecordDialog):
        if not RecordDialog.objectName():
            RecordDialog.setObjectName(u"RecordDialog")
        RecordDialog.resize(1100, 720)
        RecordDialog.setMinimumSize(QSize(900, 550))
        font = QFont()
        font.setFamilies([u"Inter"])
        RecordDialog.setFont(font)
        RecordDialog.setStyleSheet(u"/* \u2500\u2500 \u0411\u0430\u0437\u043e\u0432\u044b\u0435 \u0441\u0442\u0438\u043b\u0438 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"* {\n"
"    font-family: \"Inter\";\n"
"    font-size: 13px;\n"
"    color: #40513B;\n"
"}\n"
"\n"
"QDialog, QWidget {\n"
"    background-color: #EDF1D6;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a \u0434\u0438\u0430\u043b\u043e\u0433\u0430 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QLabel#lblTitle {\n"
"    font-size: 17px;\n"
"    font-weight: bold;\n"
"    color: #40513B;\n"
"    padding-bottom: 4px;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u041f\u043e\u0434\u043f\u0438"
                        "\u0441\u0438 \u0441\u0435\u043a\u0446\u0438\u0439 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QLabel#lblFormSection,\n"
"QLabel#lblResultsSection {\n"
"    font-size: 11px;\n"
"    font-weight: bold;\n"
"    color: #609966;\n"
"    padding-top: 4px;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0413\u043e\u0440\u0438\u0437\u043e\u043d\u0442\u0430\u043b\u044c\u043d\u044b\u0435 \u0440\u0430\u0437\u0434\u0435\u043b\u0438\u0442\u0435\u043b\u0438 (\u0442\u043e\u043b\u044c\u043a\u043e \u043d\u0430\u0448\u0438, \u043d\u0435 \u0442\u0440\u043e\u0433\u0430\u0435\u043c \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u044c) */\n"
"QFrame#divider1,\n"
"QFrame#divider2,\n"
"QFrame#dividerResults {\n"
"    background-color: #C8D8B0;\n"
"    max-height: 1px;\n"
"    border: none;\n"
"    margin: 2px 0;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0412\u044b"
                        "\u043f\u0430\u0434\u0430\u044e\u0449\u0438\u0439 \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u044c \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QCalendarWidget QWidget#qt_calendar_navigationbar {\n"
"    background-color: #40513B;\n"
"    padding: 4px 8px;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton {\n"
"    color: #fcfcee;\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 4px 10px;\n"
"    font-size: 13px;\n"
"    font-weight: bold;\n"
"    min-width: 0;\n"
"}\n"
"QCalendarWidget QToolButton:hover {\n"
"    background-color: #609966;\n"
"}\n"
"QCalendarWidget QToolButton::menu-indicator {\n"
"    image: none;\n"
"}\n"
"\n"
"/* Year spinbox \u0432\u043d\u0443\u0442\u0440\u0438 \u043a\u0430\u043b\u0435\u043d\u0434\u0430\u0440\u044f \u2014 \u043a\u0430\u043a spinbox \u0432 \u0433\u043b\u0430\u0432"
                        "\u043d\u043e\u043c \u043e\u043a\u043d\u0435 */\n"
"QCalendarWidget QSpinBox {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 4px;\n"
"    padding: 3px 28px 3px 8px;\n"
"    color: #40513B;\n"
"    font-size: 13px;\n"
"    min-width: 64px;\n"
"    selection-background-color: #9DC08B;\n"
"    selection-color: #40513B;\n"
"}\n"
"QCalendarWidget QSpinBox::up-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 22px;\n"
"    border-left: 1px solid #9DC08B;\n"
"    border-bottom: 1px solid #9DC08B;\n"
"    border-top-right-radius: 4px;\n"
"    background-color: #609966;\n"
"}\n"
"QCalendarWidget QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 22px;\n"
"    border-left: 1px solid #9DC08B;\n"
"    border-top: 1px solid #9DC08B;\n"
"    border-bottom-right-radius: 4px;\n"
"    background-color: #609966;\n"
"}\n"
"QCalendarWidget QSpinBox::up-button:hover,\n"
"Q"
                        "CalendarWidget QSpinBox::down-button:hover {\n"
"    background-color: #6DA65B;\n"
"}\n"
"QCalendarWidget QSpinBox::up-arrow {\n"
"    image: url(:/resources/images/up_arrow.svg);\n"
"    width: 8px;\n"
"    height: 5px;\n"
"}\n"
"QCalendarWidget QSpinBox::down-arrow {\n"
"    image: url(:/resources/images/down_arrow.svg);\n"
"    width: 8px;\n"
"    height: 5px;\n"
"}\n"
"\n"
"/* \u0421\u0435\u0442\u043a\u0430 \u0434\u043d\u0435\u0439 */\n"
"QCalendarWidget QAbstractItemView {\n"
"    background-color: #F8FCE0;\n"
"    alternate-background-color: #F5F8EC;\n"
"    selection-background-color: #609966;\n"
"    selection-color: #fcfcee;\n"
"    outline: none;\n"
"}\n"
"QCalendarWidget QAbstractItemView:enabled {\n"
"    color: #40513B;\n"
"}\n"
"QCalendarWidget QAbstractItemView:disabled {\n"
"    color: #C8D8B0;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u041f\u043e\u043b\u044f \u0432\u0432\u043e\u0434\u0430 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QLineEdit {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 6px 10px;\n"
"    color: #40513B;\n"
"    min-height: 28px;\n"
"}\n"
"QLineEdit:focus {\n"
"    border: 1.5px solid #609966;\n"
"}\n"
"QLineEdit:disabled {\n"
"    background-color: #EDF1D6;\n"
"    border: 1px solid #C8D8B0;\n"
"    color: #9DC08B;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u041f\u043e\u043b\u044f \u0434\u0430\u0442 \u2014 \u043a\u0430\u043a SpinBox \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QDateEdit {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 6px 28px 6px 10px;\n"
"    color: #40513B;\n"
"    min-height: 28px;\n"
""
                        "}\n"
"QDateEdit:focus {\n"
"    border: 1.5px solid #609966;\n"
"}\n"
"QDateEdit:disabled {\n"
"    background-color: #EDF1D6;\n"
"    border: 1px solid #C8D8B0;\n"
"    color: #9DC08B;\n"
"}\n"
"QDateEdit::drop-down {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: center right;\n"
"    width: 28px;\n"
"    border-left: 1px solid #9DC08B;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    background-color: #609966;\n"
"}\n"
"QDateEdit::drop-down:hover {\n"
"    background-color: #6DA65B;\n"
"}\n"
"QDateEdit::drop-down:disabled {\n"
"    background-color: #C8D8B0;\n"
"}\n"
"QDateEdit::down-arrow {\n"
"    image: url(:/resources/images/down_arrow.svg);\n"
"    width: 10px;\n"
"    height: 6px;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0412\u044b\u043f\u0430\u0434\u0430\u044e\u0449\u0438\u0439 \u0441\u043f\u0438\u0441\u043e\u043a \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QComboBox {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 5px;\n"
"    padding: 6px 28px 6px 10px;\n"
"    color: #40513B;\n"
"    min-height: 28px;\n"
"}\n"
"QComboBox:focus {\n"
"    border: 1.5px solid #609966;\n"
"}\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: center right;\n"
"    width: 28px;\n"
"    border-left: 1px solid #9DC08B;\n"
"    border-top-right-radius: 5px;\n"
"    border-bottom-right-radius: 5px;\n"
"    background-color: #609966;\n"
"}\n"
"QComboBox::drop-down:hover {\n"
"    background-color: #6DA65B;\n"
"}\n"
"QComboBox::down-arrow {\n"
"    image: url(:/resources/images/down_arrow.svg);\n"
"    width: 10px;\n"
"    height: 6px;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #9DC08B;\n"
"    selection-background-color: #609966;\n"
"    selection-color: #fcfcee;\n"
""
                        "    outline: none;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0427\u0435\u043a\u0431\u043e\u043a\u0441\u044b \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QCheckBox {\n"
"    color: #40513B;\n"
"    spacing: 6px;\n"
"}\n"
"QCheckBox::indicator {\n"
"    width: 16px;\n"
"    height: 16px;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 3px;\n"
"    background-color: #F8FCE0;\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background-color: #609966;\n"
"    border-color: #609966;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u041e\u0441\u043d\u043e\u0432\u043d\u044b\u0435 \u043a\u043d\u043e\u043f\u043a\u0438 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QPushButton {\n"
"    background-color: #609966;\n"
"    color: #fcfcee;\n"
"    border: none;\n"
"    border-radius: 6px;\n"
"    padding: 8px 20px;\n"
"    font-size: 13px;\n"
"    min-width: 80px;\n"
"}\n"
"QPushButton:hover   { background-color: #6DA65B; }\n"
"QPushButton:pressed { background-color: #40513B; }\n"
"\n"
"QPushButton#btnCancel {\n"
"    background-color: transparent;\n"
"    color: #40513B;\n"
"    border: 1px solid #9DC08B;\n"
"}\n"
"QPushButton#btnCancel:hover   { background-color: #9DC08B; color: #fcfcee; }\n"
"QPushButton#btnCancel:pressed { background-color: #609966; color: #fcfcee; }\n"
"\n"
"/* \u2500\u2500 \u041a\u043d\u043e\u043f\u043a\u0438 \u043f\u0430\u0433\u0438\u043d\u0430\u0446\u0438\u0438 (\u043a\u0430\u043a \u0432 \u0433\u043b\u0430\u0432\u043d\u043e\u043c \u043e\u043a\u043d\u0435) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QFrame#paginationBar QPushButto"
                        "n {\n"
"    background-color: #6DA65B;\n"
"    color: #fcfcee;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    min-width: 28px; max-width: 28px;\n"
"    min-height: 26px; max-height: 26px;\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    padding: 0;\n"
"}\n"
"QFrame#paginationBar QPushButton:hover    { background-color: #40513B; }\n"
"QFrame#paginationBar QPushButton:disabled { background-color: #C8D8B0; color: #9DC08B; }\n"
"\n"
"QFrame#paginationBar QLabel {\n"
"    color: #40513B;\n"
"    font-size: 12px;\n"
"    padding: 0 4px;\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* SpinBox \u0432 paginationBar \u2014 \u0441\u043e \u0441\u0442\u0440\u0435\u043b\u043a\u0430\u043c\u0438 */\n"
"QFrame#paginationBar QSpinBox {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #609966;\n"
"    border-radius: 4px;\n"
"    padding: 2px 4px;\n"
"    color: #40513B;\n"
"    min-height: 24px; max-height: 24px;\n"
"    font-size: 12px;\n"
"}\n"
"QFrame#paginationBar QSpinBox::up-butto"
                        "n {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: top right;\n"
"    width: 16px;\n"
"    background: #609966;\n"
"    border-top-right-radius: 4px;\n"
"}\n"
"QFrame#paginationBar QSpinBox::down-button {\n"
"    subcontrol-origin: border;\n"
"    subcontrol-position: bottom right;\n"
"    width: 16px;\n"
"    background: #609966;\n"
"    border-bottom-right-radius: 4px;\n"
"}\n"
"QFrame#paginationBar QSpinBox::up-button:hover,\n"
"QFrame#paginationBar QSpinBox::down-button:hover {\n"
"    background: #6DA65B;\n"
"}\n"
"QFrame#paginationBar QSpinBox::up-arrow {\n"
"    image: url(:/resources/images/up_arrow.svg);\n"
"    width: 8px;\n"
"    height: 5px;\n"
"}\n"
"QFrame#paginationBar QSpinBox::down-arrow {\n"
"    image: url(:/resources/images/down_arrow.svg);\n"
"    width: 8px;\n"
"    height: 5px;\n"
"}\n"
"\n"
"/* \u2500\u2500 \u0422\u0430\u0431\u043b\u0438\u0446\u0430 \u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u043e\u0432 \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500 */\n"
"QTableView#resultsTable {\n"
"    background-color: #F8FCE0;\n"
"    alternate-background-color: #F5F8EC;\n"
"    gridline-color: #C8D8B0;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 4px;\n"
"    selection-background-color: #9DC08B;\n"
"    selection-color: #40513B;\n"
"}\n"
"QTableView#resultsTable::item {\n"
"    padding: 5px 8px;\n"
"    border-bottom: 1px solid #E0EAC8;\n"
"}\n"
"QHeaderView::section {\n"
"    background-color: #40513B;\n"
"    color: #fcfcee;\n"
"    padding: 6px 8px;\n"
"    border: none;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"/* \u2500\u2500 SpinBox \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
                        "\u2500\u2500\u2500\u2500 */\n"
"QSpinBox {\n"
"    background-color: #F8FCE0;\n"
"    border: 1px solid #9DC08B;\n"
"    border-radius: 4px;\n"
"    padding: 3px 6px;\n"
"    color: #40513B;\n"
"}\n"
"\n"
"\n"
"QMessageBox {\n"
"    background-color: #2b2b2b;  /* \u0444\u043e\u043d \u043a\u0430\u043a \u0443 \u043f\u0440\u0438\u043b\u043e\u0436\u0435\u043d\u0438\u044f */\n"
"}\n"
"\n"
"    QMessageBox QLabel {\n"
"        color: #ffffff;\n"
"        font-size: 13px;\n"
"    }\n"
"\n"
"    QMessageBox QPushButton {\n"
"        background-color: #3c3f41;\n"
"        color: #ffffff;\n"
"        border: 1px solid #555;\n"
"        padding: 4px 16px;\n"
"        border-radius: 4px;\n"
"    }\n"
"\n"
"    QMessageBox QPushButton:hover {\n"
"        background-color: #4c5052;\n"
"    }")
        self.mainLayout = QVBoxLayout(RecordDialog)
        self.mainLayout.setSpacing(10)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(24, 20, 24, 20)
        self.lblTitle = QLabel(RecordDialog)
        self.lblTitle.setObjectName(u"lblTitle")

        self.mainLayout.addWidget(self.lblTitle)

        self.divider1 = QFrame(RecordDialog)
        self.divider1.setObjectName(u"divider1")
        self.divider1.setFrameShape(QFrame.Shape.HLine)
        self.divider1.setFrameShadow(QFrame.Shadow.Sunken)

        self.mainLayout.addWidget(self.divider1)

        self.lblFormSection = QLabel(RecordDialog)
        self.lblFormSection.setObjectName(u"lblFormSection")

        self.mainLayout.addWidget(self.lblFormSection)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout.setFormAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.formLayout.setLabelAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)
        self.formLayout.setHorizontalSpacing(10)
        self.formLayout.setVerticalSpacing(10)
        self.lblCriteriaGroup = QLabel(RecordDialog)
        self.lblCriteriaGroup.setObjectName(u"lblCriteriaGroup")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.lblCriteriaGroup)

        self.criteriaGroup = QComboBox(RecordDialog)
        self.criteriaGroup.addItem("")
        self.criteriaGroup.addItem("")
        self.criteriaGroup.addItem("")
        self.criteriaGroup.setObjectName(u"criteriaGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.criteriaGroup.sizePolicy().hasHeightForWidth())
        self.criteriaGroup.setSizePolicy(sizePolicy)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.criteriaGroup)

        self.lblName = QLabel(RecordDialog)
        self.lblName.setObjectName(u"lblName")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.lblName)

        self.fldName = QLineEdit(RecordDialog)
        self.fldName.setObjectName(u"fldName")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.fldName)

        self.lblBirth = QLabel(RecordDialog)
        self.lblBirth.setObjectName(u"lblBirth")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.lblBirth)

        self.fldBirth = QDateEdit(RecordDialog)
        self.fldBirth.setObjectName(u"fldBirth")
        self.fldBirth.setCalendarPopup(True)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.fldBirth)

        self.lblVisit = QLabel(RecordDialog)
        self.lblVisit.setObjectName(u"lblVisit")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.lblVisit)

        self.fldVisit = QDateEdit(RecordDialog)
        self.fldVisit.setObjectName(u"fldVisit")
        self.fldVisit.setCalendarPopup(True)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.fldVisit)

        self.lblVet = QLabel(RecordDialog)
        self.lblVet.setObjectName(u"lblVet")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.lblVet)

        self.fldVet = QLineEdit(RecordDialog)
        self.fldVet.setObjectName(u"fldVet")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.fldVet)

        self.lblDiag = QLabel(RecordDialog)
        self.lblDiag.setObjectName(u"lblDiag")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.lblDiag)

        self.fldDiag = QLineEdit(RecordDialog)
        self.fldDiag.setObjectName(u"fldDiag")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.fldDiag)


        self.mainLayout.addLayout(self.formLayout)

        self.resultsFrame = QFrame(RecordDialog)
        self.resultsFrame.setObjectName(u"resultsFrame")
        self.resultsFrame.setVisible(False)
        self.resultsVLayout = QVBoxLayout(self.resultsFrame)
        self.resultsVLayout.setSpacing(6)
        self.resultsVLayout.setObjectName(u"resultsVLayout")
        self.resultsVLayout.setContentsMargins(0, 0, 0, 0)
        self.dividerResults = QFrame(self.resultsFrame)
        self.dividerResults.setObjectName(u"dividerResults")
        self.dividerResults.setFrameShape(QFrame.Shape.HLine)
        self.dividerResults.setFrameShadow(QFrame.Shadow.Sunken)

        self.resultsVLayout.addWidget(self.dividerResults)

        self.lblResultsSection = QLabel(self.resultsFrame)
        self.lblResultsSection.setObjectName(u"lblResultsSection")

        self.resultsVLayout.addWidget(self.lblResultsSection)

        self.resultsTable = QTableView(self.resultsFrame)
        self.resultsTable.setObjectName(u"resultsTable")
        self.resultsTable.setMinimumSize(QSize(0, 200))
        self.resultsTable.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.resultsTable.setAlternatingRowColors(True)
        self.resultsTable.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        self.resultsVLayout.addWidget(self.resultsTable)

        self.paginationBar = QFrame(self.resultsFrame)
        self.paginationBar.setObjectName(u"paginationBar")
        self.paginationLayout = QHBoxLayout(self.paginationBar)
        self.paginationLayout.setSpacing(6)
        self.paginationLayout.setObjectName(u"paginationLayout")
        self.paginationLayout.setContentsMargins(0, 4, 0, 4)
        self.btnFirst = QPushButton(self.paginationBar)
        self.btnFirst.setObjectName(u"btnFirst")
        self.btnFirst.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnFirst)

        self.btnPrev = QPushButton(self.paginationBar)
        self.btnPrev.setObjectName(u"btnPrev")
        self.btnPrev.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnPrev)

        self.lblPageInfo = QLabel(self.paginationBar)
        self.lblPageInfo.setObjectName(u"lblPageInfo")

        self.paginationLayout.addWidget(self.lblPageInfo)

        self.btnNext = QPushButton(self.paginationBar)
        self.btnNext.setObjectName(u"btnNext")
        self.btnNext.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnNext)

        self.btnLast = QPushButton(self.paginationBar)
        self.btnLast.setObjectName(u"btnLast")
        self.btnLast.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.paginationLayout.addWidget(self.btnLast)

        self.paginationSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.paginationLayout.addItem(self.paginationSpacer)

        self.lblTotal = QLabel(self.paginationBar)
        self.lblTotal.setObjectName(u"lblTotal")

        self.paginationLayout.addWidget(self.lblTotal)

        self.lblPerPage = QLabel(self.paginationBar)
        self.lblPerPage.setObjectName(u"lblPerPage")

        self.paginationLayout.addWidget(self.lblPerPage)

        self.spinPerPage = QSpinBox(self.paginationBar)
        self.spinPerPage.setObjectName(u"spinPerPage")
        self.spinPerPage.setMinimumSize(QSize(58, 30))
        self.spinPerPage.setMaximumSize(QSize(58, 30))
        self.spinPerPage.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.spinPerPage.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.UpDownArrows)
        self.spinPerPage.setMinimum(5)
        self.spinPerPage.setMaximum(100)
        self.spinPerPage.setSingleStep(5)
        self.spinPerPage.setValue(10)

        self.paginationLayout.addWidget(self.spinPerPage)


        self.resultsVLayout.addWidget(self.paginationBar)


        self.mainLayout.addWidget(self.resultsFrame)

        self.divider2 = QFrame(RecordDialog)
        self.divider2.setObjectName(u"divider2")
        self.divider2.setFrameShape(QFrame.Shape.HLine)
        self.divider2.setFrameShadow(QFrame.Shadow.Sunken)

        self.mainLayout.addWidget(self.divider2)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setSpacing(10)
        self.buttonLayout.setObjectName(u"buttonLayout")
        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttonLayout.addItem(self.buttonSpacer)

        self.btnCancel = QPushButton(RecordDialog)
        self.btnCancel.setObjectName(u"btnCancel")

        self.buttonLayout.addWidget(self.btnCancel)

        self.btnConfirm = QPushButton(RecordDialog)
        self.btnConfirm.setObjectName(u"btnConfirm")

        self.buttonLayout.addWidget(self.btnConfirm)


        self.mainLayout.addLayout(self.buttonLayout)


        self.retranslateUi(RecordDialog)

        self.btnConfirm.setDefault(True)


        QMetaObject.connectSlotsByName(RecordDialog)
    # setupUi

    def retranslateUi(self, RecordDialog):
        RecordDialog.setWindowTitle(QCoreApplication.translate("RecordDialog", u"\u0414\u0438\u0430\u043b\u043e\u0433", None))
        self.lblTitle.setText(QCoreApplication.translate("RecordDialog", u"\u0417\u0430\u0433\u043e\u043b\u043e\u0432\u043e\u043a", None))
        self.lblFormSection.setText(QCoreApplication.translate("RecordDialog", u"\u0414\u0430\u043d\u043d\u044b\u0435 \u0437\u0430\u043f\u0438\u0441\u0438", None))
        self.lblCriteriaGroup.setText(QCoreApplication.translate("RecordDialog", u"\u0423\u0441\u043b\u043e\u0432\u0438\u0435:", None))
        self.criteriaGroup.setItemText(0, QCoreApplication.translate("RecordDialog", u"\u0418\u043c\u044f \u043f\u0438\u0442\u043e\u043c\u0446\u0430 \u0438 \u0434\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f", None))
        self.criteriaGroup.setItemText(1, QCoreApplication.translate("RecordDialog", u"\u0414\u0430\u0442\u0430 \u043f\u0440\u0438\u0451\u043c\u0430 \u0438 \u0424\u0418\u041e \u0432\u0435\u0442\u0435\u0440\u0438\u043d\u0430\u0440\u0430", None))
        self.criteriaGroup.setItemText(2, QCoreApplication.translate("RecordDialog", u"\u0424\u0440\u0430\u0437\u0430 \u0438\u0437 \u0434\u0438\u0430\u0433\u043d\u043e\u0437\u0430", None))

        self.lblName.setText(QCoreApplication.translate("RecordDialog", u"\u0418\u043c\u044f \u043f\u0438\u0442\u043e\u043c\u0446\u0430:", None))
        self.lblBirth.setText(QCoreApplication.translate("RecordDialog", u"\u0414\u0430\u0442\u0430 \u0440\u043e\u0436\u0434\u0435\u043d\u0438\u044f:", None))
        self.fldBirth.setDisplayFormat(QCoreApplication.translate("RecordDialog", u"dd.MM.yyyy", None))
        self.lblVisit.setText(QCoreApplication.translate("RecordDialog", u"\u0414\u0430\u0442\u0430 \u043f\u043e\u0441\u043b. \u043f\u0440\u0438\u0451\u043c\u0430:", None))
        self.fldVisit.setDisplayFormat(QCoreApplication.translate("RecordDialog", u"dd.MM.yyyy", None))
        self.lblVet.setText(QCoreApplication.translate("RecordDialog", u"\u0424\u0418\u041e \u0432\u0435\u0442\u0435\u0440\u0438\u043d\u0430\u0440\u0430:", None))
        self.lblDiag.setText(QCoreApplication.translate("RecordDialog", u"\u0414\u0438\u0430\u0433\u043d\u043e\u0437:", None))
        self.lblResultsSection.setText(QCoreApplication.translate("RecordDialog", u"\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u044b", None))
#if QT_CONFIG(tooltip)
        self.btnFirst.setToolTip(QCoreApplication.translate("RecordDialog", u"\u041f\u0435\u0440\u0432\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnFirst.setText(QCoreApplication.translate("RecordDialog", u"\u23ee", None))
#if QT_CONFIG(tooltip)
        self.btnPrev.setToolTip(QCoreApplication.translate("RecordDialog", u"\u041f\u0440\u0435\u0434\u044b\u0434\u0443\u0449\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnPrev.setText(QCoreApplication.translate("RecordDialog", u"\u25c0", None))
        self.lblPageInfo.setText(QCoreApplication.translate("RecordDialog", u"\u0421\u0442\u0440. 1 / 1", None))
#if QT_CONFIG(tooltip)
        self.btnNext.setToolTip(QCoreApplication.translate("RecordDialog", u"\u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnNext.setText(QCoreApplication.translate("RecordDialog", u"\u25b6", None))
#if QT_CONFIG(tooltip)
        self.btnLast.setToolTip(QCoreApplication.translate("RecordDialog", u"\u041f\u043e\u0441\u043b\u0435\u0434\u043d\u044f\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430", None))
#endif // QT_CONFIG(tooltip)
        self.btnLast.setText(QCoreApplication.translate("RecordDialog", u"\u23ed", None))
        self.lblTotal.setText(QCoreApplication.translate("RecordDialog", u"\u0412\u0441\u0435\u0433\u043e: 0", None))
        self.lblPerPage.setText(QCoreApplication.translate("RecordDialog", u"\u041d\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0435:", None))
        self.btnCancel.setText(QCoreApplication.translate("RecordDialog", u"\u041e\u0442\u043c\u0435\u043d\u0430", None))
        self.btnConfirm.setText(QCoreApplication.translate("RecordDialog", u"OK", None))
    # retranslateUi

