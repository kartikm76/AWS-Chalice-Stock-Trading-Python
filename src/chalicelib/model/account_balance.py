from sqlalchemy import Boolean, Column, Integer, String, Date, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from chalicelib.utils.database_connect import Base

class AccountBalanceORM(Base):
    __tablename__ = "account_balance"

    account_id = Column(Integer, primary_key=True, index=True)
    balance_amount = Column(Float)
    as_of_date = Column(Date)