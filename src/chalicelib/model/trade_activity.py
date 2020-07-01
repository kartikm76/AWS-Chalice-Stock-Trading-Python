import uuid
from chalicelib.utils.database_connect import Base
from sqlalchemy.orm import *
import sqlalchemy.types as types
from sqlalchemy import Column, String, Integer, Float, Date
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


class GUID(types.TypeDecorator):
    impl = String(50)

    def process_bind_param(self, value, dialect):
        if value is not None:
            return "%.32x" % int(value)
        else:
            return None

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid.UUID(str(value))


class TradeActivityORM(Base):
    __tablename__ = "trade_activity"
    transaction_id = Column(GUID(as_uuid=True), primary_key=True,
                            default=uuid.uuid4, unique=True, nullable=False)
    account_id = Column(Integer)
    security_symbol = Column(String(10))
    transaction_qty = Column(Integer)
    security_price = Column(Float)
    transaction_type_code = Column(String(1))
    transaction_timestamp = Column(Date)
