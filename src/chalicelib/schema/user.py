from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from chalicelib.utils.database_connect import Base
from pydantic import BaseModel, constr
from typing import List

class UserSchema(BaseModel):
    id: str
    name: str
    ssn: str
    isActive: str

    class Config:
        orm_mode = True