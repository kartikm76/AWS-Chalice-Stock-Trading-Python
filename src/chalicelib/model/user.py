from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from chalicelib.utils.database_connect import Base

class User(Base):
    __tablename__ = "user_master"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)