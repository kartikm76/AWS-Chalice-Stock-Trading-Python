from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from chalicelib.utils.database_connect import Base


class AccountORM(Base):
    __tablename__ = "account_master"
    
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(20))
    open_date = Column(Date)
    is_active = Column(String(1))