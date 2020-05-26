import json
import requests
from chalicelib.model.stock import StockORM
from chalicelib.utils.constants import *

class StockTradeService:

    return_payload = {
        "code": None,
        "message": None        
    }

    #1. input required - account_id, stock_symbol, direction - B/S, qty, price - will be determined by market price
    #2. if stock does not exist in stock_holding; add
    #3. if stock does exist in stock_holding; adjust its qty depending upon B/S
    #4. update account_balance
    #5. log into trade_activity
    
    def stock_trade(self, session, payload):