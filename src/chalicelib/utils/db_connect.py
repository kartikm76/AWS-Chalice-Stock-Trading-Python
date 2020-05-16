#from chalicelib import settings
import peewee as pw
import logging

logger = logging.getLogger('peewee')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

# db_connect = pw.MySQLDatabase(host=settings.DATABASE['HOST'],
#                               port=settings.DATABASE['PORT'],
#                               user=settings.DATABASE['USER'],
#                               passwd=settings.DATABASE['PASSWORD'],
#                               database=settings.DATABASE['NAME'])

db_connect = pw.MySQLDatabase(
    host="stock-trading.cufofj0atk2l.us-east-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="password",
    database="stock-trading")
