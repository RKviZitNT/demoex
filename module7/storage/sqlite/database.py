import sqlite3


class Database:
    def __init__(self, path="orders.db"):
        self.path = path
        self.init_db()

    def connect(self):
        return sqlite3.connect(self.path)

    def init_db(self):
        with self.connect() as conn:
            cur = conn.cursor()

            cur.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client TEXT,
                city TEXT,
                phone TEXT,
                date TEXT,
                amount REAL
            )
            """)

            cur.execute("SELECT COUNT(*) FROM Orders")
            if cur.fetchone()[0] == 0:
                cur.executemany("""
                INSERT INTO Orders (client, city, phone, date, amount)
                VALUES (?, ?, ?, ?, ?)
                """, [
                    ("ООО 'Ассоль'", "Калуга", "+79184572398", "06.06.2026", 2488),
                    ("ООО 'Квант'", "Железноводск", "+79884581555", "15.06.2026", 15800),
                    ("ООО 'Поставка'", "Пятигорск", "+79198634592", "21.07.2026", 125000),
                ])