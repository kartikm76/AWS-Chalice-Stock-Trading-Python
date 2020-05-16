from peewee import Model, CharField, DateField, FloatField
from chalicelib.model.base_model import MySQLModel

class AccountBalance(MySQLModel):    
    account_id = CharField()
    balance_amount = FloatField()
    as_of_date = DateField()

    class Meta:
        table_name = 'account_balance'