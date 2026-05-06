from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, service):
        super().__init__()
        uic.loadUi("ui/main_window.ui", self)

        self.service = service

        self.bind_events()
        self.load_data()

    def bind_events(self):
        self.btnFilter.clicked.connect(self.filter_data)
        self.btnShowAll.clicked.connect(self.load_data)
        self.btnSearch.clicked.connect(self.search)
        self.radioAsc.toggled.connect(self.sort)
        self.radioDesc.toggled.connect(self.sort)

    def load_data(self):
        try:
            data = self.service.get_all()
            self.fill_table(data)
            self.load_clients()
        except Exception as e:
            self.show_error(e)

    def fill_table(self, rows):
        self.tableOrders.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.tableOrders.setItem(i, j, QTableWidgetItem(str(value)))

        self.update_stats(rows)

    def update_stats(self, rows):
        count = len(rows)
        total = sum(float(r[4]) for r in rows)

        self.labelCount.setText(f"Всего заказов: {count}")
        self.labelSum.setText(f"Общая сумма: {total}")

    def load_clients(self):
        self.comboClients.clear()
        self.comboClients.addItems(self.service.get_clients())

    def filter_data(self):
        try:
            client = self.comboClients.currentText()
            data = self.service.filter_by_client(client)
            self.fill_table(data)
        except Exception as e:
            self.show_error(e)

    def sort(self):
        try:
            field_map = {
                "Заказчик": "client",
                "Дата заказа": "date",
                "Сумма заказа": "amount"
            }

            field = field_map.get(self.listSortFields.currentText(), "client")
            order = "ASC" if self.radioAsc.isChecked() else "DESC"

            data = self.service.sort(field, order)
            self.fill_table(data)
        except Exception as e:
            self.show_error(e)

    def search(self):
        try:
            text = self.lineSearch.text()
            if not text:
                QMessageBox.information(self, "Поиск", "Введите текст")
                return

            data = self.service.search(text)
            self.fill_table(data)

            for row in range(self.tableOrders.rowCount()):
                for col in range(self.tableOrders.columnCount()):
                    item = self.tableOrders.item(row, col)
                    if text.lower() in item.text().lower():
                        item.setBackground(Qt.GlobalColor.yellow)

        except Exception as e:
            self.show_error(e)

    def show_error(self, e):
        QMessageBox.critical(self, "Ошибка", str(e))