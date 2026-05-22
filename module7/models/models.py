from peewee import *

from storage.postgres.database import database


class BaseModel(Model):

    class Meta():
        database = database


class Client(BaseModel):

    name = CharField()
    city = CharField()
    phone = CharField()

    def __str__(self):
        return self.name
    

class Order(BaseModel):
    
    client = ForeignKeyField(Client, backref="orders")
    order_date = DateField()
    total_amount = DecimalField(max_digits=12, decimal_places=2)