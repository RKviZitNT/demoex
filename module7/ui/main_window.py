from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox
)

from services.orders_service import OrdersService

from ui.main_window_ui import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.query = None

        self.load_clients()
        self.load_orders()
        self.sort_orders()

        self.btnFilter.clicked.connect(self.filter_orders)
        self.btnShowAll.clicked.connect(self.load_orders)
        self.btnSearch.clicked.connect(self.search)

        self.comboSelectSortField.currentTextChanged.connect(self.sort_orders)

        self.radioAsc.clicked.connect(self.sort_orders)
        self.radioDesc.clicked.connect(self.sort_orders)

    def load_clients(self):
        self.comboSelectClient.clear()

        for client in OrdersService.get_clients():
            self.comboSelectClient.addItem(client.name, client.id)

    def load_orders(self):
        self.query = OrdersService.get_orders()

        self.fill_table()

    def fill_table(self):
        orders = list(self.query)

        self.tableOrders.setRowCount(len(orders))

        for row, order in enumerate(orders):
            data = [
                order.client.name,
                order.client.city,
                order.client.phone,
                str(order.order_date),
                str(order.products_quantity),
            ]

            for column, value in enumerate(data):
                self.tableOrders.setItem(row, column, QTableWidgetItem(value))

        self.labelTotalOrders.setText(f"Всего заказов: {len(orders)}")
        self.labelTotalOrderedProducts.setText(f"Всего заказанной продукции: {OrdersService.total_products_quantity(self.query)}")

    def filter_orders(self):
        client = self.comboSelectClient.currentData()

        self.query = OrdersService.filter_orders(client)

        self.fill_table()

    def sort_orders(self):
        field_name = self.comboSelectSortField.currentText()
        is_asc = self.radioAsc.isChecked()

        self.query = OrdersService.sort_orders(OrdersService.get_orders(), field_name, is_asc)

        self.fill_table()

    def search(self):
        text = self.lineSearch.text().lower()

        if not text:
            self.show_info("Введите строку для поиска")
            return

        found = False

        for row in range(self.tableOrders.rowCount()):
            for column in range(self.tableOrders.columnCount()):
                item = self.tableOrders.item(row, column)

                if not item:
                    continue

                item.setBackground(QBrush())

                if text in item.text().lower():
                    item.setBackground(QColor(0, 100, 100))

                    found = True

        if not found:
            self.show_info("Ничего не найдено")



    def show_info(self, message):
        QMessageBox.information(self, "Информация", message)