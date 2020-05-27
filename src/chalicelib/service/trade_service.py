import datetime
from pydantic import BaseModel, Field, ValidationError
from chalicelib.model.stock_holding import StockHoldingORM
from chalicelib.model.account_balance import AccountBalanceORM
from chalicelib.schema.trade import TradeSchema
from chalicelib.service.account_balance_service import AccountBalanceService
from chalicelib.service.security_lookup_service import SecurityLookUpService
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
        trade_instruction = ""
        try:
            # validate income json request
            trade_instruction = TradeSchema.parse_obj(payload)
        except ValidationError as e:
            self.return_payload['status'] = ERROR_CODE
            self.return_payload['message'] = e.errors()
            return self.return_payload

        # First get the market price for the given stock to check if the stock can be bought
        if trade_instruction.direction == 'B':
            security_look_up = SecurityLookUpService()
            security_details = security_look_up.get_security_details(trade_instruction.symbol)
            securrity_price = security_details["body"][0]["name"])
            print ("Sec Details: ", security_details["body"][0]["name"])
                                               
            # Get the account balance of the specific account
            account_bal_service = AccountBalanceService()            
            account_balance  = account_bal_service.get_account_balance(session, trade_instruction.account_id, as_of_date=datetime.date.today())
            print ("Acc Balance: ", str(account_balance))
            ##if account_balance >= trade_instruction.quantity * security.price:

                #     # start a transaction
                #     transaction = session.create_transaction()
                #     try:
                #         stock_holding = session.query(StockHoldingORM).filter((StockHoldingORM.account_id == trade_instruction.account_id)                                                                            
                #                                                             & (StockHoldingORM.stock_symbol == trade_instruction.symbol)).first()
                #         if stock_holding.scalar():

                #             # add stock holding qty
                #             updated_stock_holding = stock_holding["holding_qty"] + trade_instruction.quantity

                #             # update account balance
                #             updated_balance = account_balance - (trade_instruction.quantity * security.price)

                #         transaction.commit()
                #     except:
                #         transaction.rollback()                        
                #         raise Exception
                # else:
                #     self.return_payload['status'] = ERROR_CODE
                #     self.return_payload['message'] = "Not enough balance to buy: " + trade_instruction.symbol
                #     return self.return_payload        

                        
                                                                
                        # call the method to update trade activity log
                        # close the transaction
                    # if not okay - return an error message
                # if trade_instruction.direction = 'S':                 
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
            self.return_payload['message'] = trade_instruction.symbol + " trade executed successfully"
        return self.return_payload





#stock_holding = session.query(StockHoldingORM).filter((StockHoldingORM.stock_symbol == trade_instruction.symbol)
#                                                                & (StockHoldingORM.account_id == trade_instruction.account_id)).first()
#
#        if stock_holding.scalar():