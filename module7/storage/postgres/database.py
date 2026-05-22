from peewee import PostgresqlDatabase


database = PostgresqlDatabase(
    "orders_db",
    user="user",
    password="pass",
    host="localhost",
    port=5432
)