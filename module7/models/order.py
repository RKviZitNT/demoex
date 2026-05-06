class Order:
    def __init__(self, client, city, phone, date, amount):
        self.client = client
        self.city = city
        self.phone = phone
        self.date = date
        self.amount = float(amount)