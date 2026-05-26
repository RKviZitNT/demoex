from peewee import PostgresqlDatabase


DB = PostgresqlDatabase(
    'demka',
    user="user",
    password="pass",
    host="localhost",
    port=5432
)