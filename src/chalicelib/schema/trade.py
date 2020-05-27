from pydantic import BaseModel, constr, ValidationError, validator
import re
from typing import List

class TradeSchema(BaseModel):
    #1. input required - account_id, stock_symbol, direction - B/S, qty, price - will be determined by market price
    account_id: int
    symbol: str
    direction: str
    quantity: float
            
    class Config:
        orm_mode = True