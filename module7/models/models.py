from peewee import *

from storage.postgres.database import DB


class BaseModel(Model):

    class Meta:
        database = DB


class Clients(BaseModel):

    class Meta:
        table_name = "Clients"

    name = CharField()
    city = CharField()
    phone = CharField()


class Manufacturer(BaseModel):

    class Meta:
        table_name = "Manufacturer"

    name = CharField()
    description = TextField()
    phone = CharField()
    email = CharField()


class Orders(BaseModel):

    class Meta:
        table_name = "Orders"

    manufacturer = ForeignKeyField(Manufacturer, backref="orders", column_name="manufacturer_id")
    client = ForeignKeyField(Clients, backref="orders", column_name="client_id")
    total_amount = DecimalField()
    products_quantity = DecimalField()
    order_date = DateTimeField()