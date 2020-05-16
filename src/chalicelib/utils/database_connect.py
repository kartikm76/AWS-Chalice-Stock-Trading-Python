from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://admin:password@stock-trading.cufofj0atk2l.us-east-1.rds.amazonaws.com:3306/stock-trading'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=False
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()

Base = declarative_base()

# logger = logging.getLogger('sqlalchemy')
# logger.addHandler(logging.StreamHandler())
# logger.setLevel(logging.INFO)