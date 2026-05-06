class OrderService:
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self._exec("SELECT client, city, phone, date, amount FROM Orders")

    def filter_by_client(self, client):
        return self._exec(
            "SELECT client, city, phone, date, amount FROM Orders WHERE client=?",
            (client,)
        )

    def sort(self, field, order):
        query = f"""
        SELECT client, city, phone, date, amount
        FROM Orders
        ORDER BY {field} {order}
        """
        return self._exec(query)

    def search(self, text):
        pattern = f"%{text}%"
        return self._exec("""
        SELECT client, city, phone, date, amount
        FROM Orders
        WHERE client LIKE ? OR city LIKE ? OR phone LIKE ? OR date LIKE ?
        """, (pattern, pattern, pattern, pattern))

    def get_clients(self):
        with self.db.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT client FROM Orders")
            return [row[0] for row in cur.fetchall()]

    def _exec(self, query, params=()):
        with self.db.connect() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()