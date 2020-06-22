from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from chalicelib.utils.database_connect import Base


class UserORM(Base):
    __tablename__ = "user_master"

    user_id = Column(String(20), primary_key=True, index=True)
    name = Column(String(45))
    ssn = Column(String(15))
    is_active = Column(String(1))
    profile_create_date = Column(Date)

    # def __repr__(self):
    #     return "<User(id='{0}', name='{1}', ssn='{2}')>".format(
    #         self.name, self.fullname, self.nickname)
