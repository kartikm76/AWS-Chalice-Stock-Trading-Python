from sqlalchemy import Column, String
from chalicelib.utils.database_connect import Base

class StockORM(Base):
    __tablename__ = "stock_master"
    
    symbol = Column(String, primary_key=True, index=True)
    name = Column(String)
