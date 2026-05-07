class OrderService:
    def __init__(self, db):
        self.db = db

    BASE_QUERY = """
    SELECT
        Customers.CustomerName,
        Customers.City,
        Customers.Phone,
        Orders.OrderDate,
        Orders.OrderAmount
    FROM Orders
    INNER JOIN Customers
        ON Orders.CustomerID = Customers.CustomerID
    """

    def get_all(self):
        return self._execute(self.BASE_QUERY)

    def get_customers(self):
        query = """
        SELECT CustomerName
        FROM Customers
        ORDER BY CustomerName
        """

        with self.db.connect() as conn:
            cur = conn.cursor()

            cur.execute(query)

            return [row[0] for row in cur.fetchall()]

    def filter_by_customer(self, customer_name):
        query = self.BASE_QUERY + """
        WHERE Customers.CustomerName = ?
        """

        return self._execute(query, (customer_name,))

    def sort(self, field, order):
        field_map = {
            "customer": "Customers.CustomerName",
            "date": "Orders.OrderDate",
            "amount": "Orders.OrderAmount"
        }

        sql_field = field_map.get(
            field,
            "Customers.CustomerName"
        )

        query = self.BASE_QUERY + f"""
        ORDER BY {sql_field} {order}
        """

        return self._execute(query)

    def search(self, text):
        pattern = f"%{text}%"

        query = self.BASE_QUERY + """
        WHERE
            Customers.CustomerName LIKE ?
            OR Customers.City LIKE ?
            OR Customers.Phone LIKE ?
            OR Orders.OrderDate LIKE ?
            OR CAST(Orders.OrderAmount AS TEXT) LIKE ?
        """

        return self._execute(query, (
            pattern,
            pattern,
            pattern,
            pattern,
            pattern
        ))

    def _execute(self, query, params=()):
        with self.db.connect() as conn:
            cur = conn.cursor()

            cur.execute(query, params)

            return cur.fetchall()