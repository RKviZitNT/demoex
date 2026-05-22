from datetime import date

from models.models import Client, Order
from storage.postgres.database import database

def main():
    database.connect()
    database.create_tables([Client, Order])

    client1 = Client.create(
        name='ООО "Текстиль"',
        city='Москва',
        phone='111-111'
    )

    client2 = Client.create(
        name='ООО "Электроника"',
        city='Казань',
        phone='222-222'
    )

    client3 = Client.create(
        name='ООО "Альянс"',
        city='Владивосток',
        phone='333-333'
    )

    Order.create(
        client=client1,
        order_date=date.today(),
        total_amount=1500
    )

    Order.create(
        client=client2,
        order_date=date.today(),
        total_amount=2300
    )

    Order.create(
        client=client3,
        order_date=date.today(),
        total_amount=3500
    )

    database.close()

if __name__ == "__main__":
    main()