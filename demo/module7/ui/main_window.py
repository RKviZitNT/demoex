from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem
)


class MainWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()

        uic.loadUi("ui/main_window.ui", self)

        self.service = service

        self.setup_table()
        self.bind_events()

        self.load_customers()
        self.load_data()

    def setup_table(self):
        self.tableOrders.setColumnCount(5)

        self.tableOrders.setHorizontalHeaderLabels([
            "Заказчик",
            "Город",
            "Телефон",
            "Дата заказа",
            "Сумма заказа"
        ])

        self.tableOrders.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tableOrders.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.tableOrders.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

    def bind_events(self):
        self.btnFilter.clicked.connect(self.filter_data)

        self.btnShowAll.clicked.connect(
            self.load_data
        )

        self.btnSearch.clicked.connect(
            self.search_data
        )

        self.radioAsc.toggled.connect(
            self.sort_data
        )

        self.radioDesc.toggled.connect(
            self.sort_data
        )

    def load_customers(self):
        try:
            self.comboClients.clear()

            customers = self.service.get_customers()

            self.comboClients.addItems(customers)

        except Exception as e:
            self.show_error(e)

    def load_data(self):
        try:
            rows = self.service.get_all()

            self.fill_table(rows)

        except Exception as e:
            self.show_error(e)

    def fill_table(self, rows):
        self.tableOrders.clearContents()

        self.tableOrders.setRowCount(
            len(rows)
        )

        for row_index, row_data in enumerate(rows):

            for col_index, value in enumerate(row_data):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                self.tableOrders.setItem(
                    row_index,
                    col_index,
                    item
                )

        self.update_statistics(rows)

    def update_statistics(self, rows):
        count = len(rows)

        total = sum(
            float(row[4])
            for row in rows
        )

        self.labelCount.setText(
            f"Всего заказов: {count}"
        )

        self.labelSum.setText(
            f"Общая сумма: {total:.2f}"
        )

    def filter_data(self):
        try:
            customer = (
                self.comboClients.currentText()
            )

            rows = self.service.filter_by_customer(
                customer
            )

            self.fill_table(rows)

        except Exception as e:
            self.show_error(e)

    def sort_data(self):
        try:
            field_map = {
                "Заказчик": "customer",
                "Дата заказа": "date",
                "Сумма заказа": "amount"
            }

            selected = (
                self.listSortFields.currentText()
            )

            field = field_map.get(
                selected
            )

            order = "ASC"

            if self.radioDesc.isChecked():
                order = "DESC"

            rows = self.service.sort(
                field,
                order
            )

            self.fill_table(rows)

        except Exception as e:
            self.show_error(e)

    def search_data(self):
        try:
            text = (
                self.lineSearch
                .text()
                .strip()
            )

            if not text:
                QMessageBox.information(
                    self,
                    "Поиск",
                    "Введите строку поиска"
                )
                return

            rows = self.service.search(text)

            self.fill_table(rows)

            for row in range(
                self.tableOrders.rowCount()
            ):

                for col in range(
                    self.tableOrders.columnCount()
                ):

                    item = self.tableOrders.item(
                        row,
                        col
                    )

                    if item is None:
                        continue

                    item.setBackground(
                        Qt.GlobalColor.white
                    )

                    if (
                        text.lower()
                        in item.text().lower()
                    ):
                        item.setBackground(
                            Qt.GlobalColor.yellow
                        )

        except Exception as e:
            self.show_error(e)

    def show_error(self, error):
        QMessageBox.critical(
            self,
            "Ошибка",
            str(error)
        )