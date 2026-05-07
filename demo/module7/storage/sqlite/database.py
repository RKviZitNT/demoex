import sqlite3


class Database:
    def __init__(self, path="orders.db"):
        self.path = path
        self.init_db()

    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def init_db(self):
        with self.connect() as conn:
            cur = conn.cursor()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS Customers (
                CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerName TEXT NOT NULL,
                City TEXT,
                Phone TEXT
            )
            """)

            cur.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
                CustomerID INTEGER NOT NULL,
                OrderDate TEXT NOT NULL,
                OrderAmount REAL NOT NULL,
                FOREIGN KEY (CustomerID)
                    REFERENCES Customers(CustomerID)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
            """)

            cur.execute("SELECT COUNT(*) FROM Customers")

            if cur.fetchone()[0] == 0:
                cur.executemany("""
                INSERT INTO Customers
                (CustomerName, City, Phone)
                VALUES (?, ?, ?)
                """, [
                    ('ООО "Ассоль"', 'Калуга', '+79184072398'),
                    ('ООО "Компьютер Квант"', 'Железноводск', '+79884581555'),
                    ('ООО "Поставка"', 'Пятигорск', '+79198634592')
                ])

                cur.executemany("""
                INSERT INTO Orders
                (CustomerID, OrderDate, OrderAmount)
                VALUES (?, ?, ?)
                """, [
                    (1, '2026-06-06', 2488.00),
                    (2, '2026-06-15', 16800.00),
                    (3, '2026-07-21', 128000.00)
                ])