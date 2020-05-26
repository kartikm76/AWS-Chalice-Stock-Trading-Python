import json
import requests
from pydantic import BaseModel, Field, ValidationError
from chalicelib.model.stock import StockORM
from chalicelib.schema.trade import TradeSchema
from chalicelib.utils.constants import *

class TradeService:

    return_payload = {
        "status": None,
        "message": None        
    }

    #1. input required - account_id, stock_symbol, direction - B/S, qty, price - will be determined by market price
    #2. if stock does not exist in stock_holding; add
    #3. if stock does exist in stock_holding; adjust its qty depending upon B/S
    #4. update account_balance
    #5. log into trade_activity

    def trade(self, session, payload):
        try:
            trade_instruction = TradeSchema.parse_obj(payload)
            
            stock_holding = session.query(StockHoldingORM).filter(StockHoldingORM.stock_symbol == trade_instruction.stock_symbol 
                                                                & StockHoldingORM.account_id == trade_instruction.account_id).first()
            if stock_holding.scalar():
                # stock exists in portfolio
                if trade_instruction.direction = 'B':
                    # check stocks * price >= account_balance
                    # if okay:
                        # start a transaction
                        # add stock holding qty                    
                        # update account balance
                        # call the method to update trade activity log
                        # close the transaction
                    # if not okay - return an error message
                if trade_instruction.direction = 'S':                 
                    # check number of stocks to sell <= stocks in holding
                    # if okay:
                        # start a transaction
                        # subtract stock holding qty
                        # update account balance
                        # call the method to update trade activity log
                        # close the transaction
                    # if not okay - return an error message
                    
            print ("Trade: ", trade_instruction)
            self.return_payload['status'] = SUCCESS_CODE
            self.return_payload['message'] = payload["stock_symbol"] + " trade executed successfully"
        except ValidationError as e:
            self.return_payload['status'] = ERROR_CODE
            self.return_payload['message'] = e.errors()            
        return self.return_payload
