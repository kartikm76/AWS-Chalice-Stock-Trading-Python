from peewee import Model, CharField, DateField
from chalicelib.utils.db_connect import db_connect


class MySQLModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = db_connect

        def __enter__(self):
            print("Connected to MySQL database")

        def __exit__(self):
            print("Exiting...")
            db_connect.close()


class User(MySQLModel):
    id = CharField()
    name = CharField()

    class Meta:
        table_name = 'user_master'
