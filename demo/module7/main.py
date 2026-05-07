import sys

from PyQt6.QtWidgets import QApplication

from services.order_service import OrderService
from storage.sqlite.database import Database
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    db = Database()

    service = OrderService(db)

    window = MainWindow(service)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()