from peewee import SelectQuery

from models.models import Clients, Orders


class OrdersService:

    @staticmethod
    def get_clients():
        return Clients.select()

    @staticmethod
    def get_orders():
        return Orders.select(Orders, Clients).join(Clients)

    @staticmethod
    def filter_orders(client):
        return Orders.select(Orders, Clients).join(Clients).where(Orders.client == client)

    @staticmethod
    def sort_orders(query: SelectQuery, field_name, is_asc):
        fields = {
            "Заказчик": Clients.name,
            "Город": Clients.city,
            "Количество продукции": Orders.products_quantity,
        }

        field = fields[field_name]

        return query.order_by(field.asc() if is_asc else field.desc())

    @staticmethod
    def total_products_quantity(query: SelectQuery):
        return sum(order.products_quantity or 0 for order in query)