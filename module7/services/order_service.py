from peewee import fn

from models.models import Client, Order


class OrderService:

    @staticmethod
    def get_clients():
        
        return Client.select()
    
    @staticmethod
    def get_orders():

        return Order.select(Order, Client).join(Client)
    
    @staticmethod
    def filter_by_client(client_id):

        return Order.select(Order, Client).join(Client).where(Client.id == client_id)
    
    @staticmethod
    def sort_orders(query, field_name, is_asc):

        fields = {
            "Заказчик": Client.name,
            "Дата заказа": Order.order_date,
            "Сумма заказа": Order.total_amount,
        }

        field = fields[field_name]

        if is_asc:
            return query.order_by(field.asc())
        
        return query.order_by(field.desc())
    
    @staticmethod
    def get_total_amount(query):

        total = query.select(fn.SUM(Order.total_amount)).scalar()

        if total is None:
            return 0
        
        return total