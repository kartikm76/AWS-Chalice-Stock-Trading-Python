from sqlalchemy import Column, String, Float, Integer
from chalicelib.utils.database_connect import Base

class StockHoldingORM(Base):
    __tablename__ = "stock_holding"
    
    account_id = Column(Integer, primary_key=True, index=True)
    security_symbol = Column(String(10), primary_key=True, index=True)
    holding_qty = Column(Float)
    purchase_price = Column(Float)