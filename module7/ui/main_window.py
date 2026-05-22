from PyQt6 import uic
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QMainWindow,
    QTableWidgetItem,
    QMessageBox
)
from models.models import Client, Order
from services.order_service import OrderService


class MainWindow(QMainWindow):
    
    def __init__(self):

        super().__init__()

        uic.loadUi("ui/main_window.ui", self)

        self.setMinimumSize(895, 645)

        self.current_query = None

        self.load_data()
        self.load_clients()

        self.btnFilter.clicked.connect(self.filter_orders)
        self.btnShowAll.clicked.connect(self.show_all_orders)
        self.btnSearch.clicked.connect(self.search_text)

        self.radioAsc.toggled.connect(self.sort_orders)
        self.radioDesc.toggled.connect(self.sort_orders)
        self.listSortFields.currentIndexChanged.connect(self.sort_orders)

    def load_clients(self):

        self.comboClients.clear()

        clients = OrderService.get_clients()

        for client in clients:
            self.comboClients.addItem(client.name, client.id)

    def load_data(self):

        try:
            query = OrderService.get_orders()

            self.current_query = query

            self.fill_table(query)

        except Exception as error:
            self.show_error(str(error))

    def fill_table(self, query):

        orders = list(query)

        self.tableOrders.setRowCount(len(orders))

        for row, order in enumerate(orders):
            self.tableOrders.setItem(row, 0, QTableWidgetItem(order.client.name))
            self.tableOrders.setItem(row, 1, QTableWidgetItem(order.client.city))
            self.tableOrders.setItem(row, 2, QTableWidgetItem(order.client.phone))
            self.tableOrders.setItem(row, 3, QTableWidgetItem(str(order.order_date)))
            self.tableOrders.setItem(row, 4, QTableWidgetItem(str(order.total_amount)))

        self.update_info(query)

    def update_info(self, query):

        count = query.count()

        total_amount = OrderService.get_total_amount(query)

        self.labelCount.setText(f'Всего заказов: {count}')
        self.labelSum.setText(f'Общая сумма: {total_amount}')

    def filter_orders(self):

        try:
            client_id = self.comboClients.currentData()

            query = OrderService.filter_by_client(client_id)

            self.current_query = query

            self.fill_table(query)

        except Exception as error:
            self.show_error(str(error))

    def show_all_orders(self):

        self.load_data()

    def sort_orders(self):

        try:
            if self.current_query is None:
                return

            field_name = self.listSortFields.currentText()

            is_asc = self.radioAsc.isChecked()

            query = OrderService.sort_orders(self.current_query, field_name, is_asc)

            self.fill_table(query)

        except Exception as error:
            self.show_error(str(error))

    def search_text(self):

        text = self.lineSearch.text().lower().strip()

        if text == '':
            QMessageBox.information(self, 'Информация', 'Введите строку поиска')
            return

        found = False

        for row in range(self.tableOrders.rowCount()):

            for column in range(self.tableOrders.columnCount()):

                item = self.tableOrders.item(row, column)

                item.setBackground(QColor('white'))

                if text in item.text().lower():

                    found = True

                    item.setBackground(QColor('yellow'))

        if not found:
            QMessageBox.information(self, 'Информация', 'Совпадений не найдено')
    
    def show_error(self, message):

        QMessageBox.critical(self, 'Ошибка', message)