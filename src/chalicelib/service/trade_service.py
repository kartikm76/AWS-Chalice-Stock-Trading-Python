import datetime
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from chalicelib.model.security_holding import SecurityHoldingORM
from chalicelib.model.account_balance import AccountBalanceORM
from chalicelib.schema.trade import TradeSchema
from chalicelib.service.account_balance_service import AccountBalanceService
from chalicelib.service.security_lookup_service import SecurityLookUpService
from chalicelib.utils.constants import API_KEY, SUCCESS_CODE, ERROR_CODE, FATAL_CODE


class TradeService:

    return_payload = {
        "status": None,
        "message": None
    }

    def trade(self, session, payload):
        trade_instruction = ""
        trade_value = ""
        try:
            # validate income json request
            trade_instruction = TradeSchema.parse_obj(payload)
            security_look_up = SecurityLookUpService()

            # Get the market price of the security to be traded
            security_details = security_look_up.get_security_details(
                trade_instruction.symbol)
            security_price = security_details["body"][0]["price"]

            trade_value = trade_instruction.quantity * security_price

            # Get the account balance of the specific account
            account_bal_service = AccountBalanceService()
            account_balance_row = account_bal_service.get_account_balance(
                session, trade_instruction.account_id)

            if account_balance_row:
                existing_account_balance = account_balance_row[0]['balance_amount']
            else:
                self.return_payload['status'] = ERROR_CODE
                self.return_payload['message'] = "Account '{0}'".format(
                    trade_instruction.account_id) + " - balance could not be retrieved"
                return self.return_payload
        except ValidationError as e:
            self.return_payload['status'] = ERROR_CODE
            self.return_payload['message'] = e.errors()
            return self.return_payload

        # if the security is to be bought
        if trade_instruction.direction == 'B':
            # Exit; if not sufficient balance
            if existing_account_balance < trade_value:
                self.return_payload['status'] = ERROR_CODE
                self.return_payload['message'] = "Not enough balance to buy: " + \
                    trade_instruction.symbol
                return self.return_payload

            # start a transaction
            try:
                security_holding = session.query(SecurityHoldingORM).filter((SecurityHoldingORM.account_id == trade_instruction.account_id)
                                                                            & (SecurityHoldingORM.security_symbol == trade_instruction.symbol)).first()
                if security_holding is None:
                    security_holding = SecurityHoldingORM()
                    security_holding.account_id = trade_instruction.account_id
                    security_holding.security_symbol = trade_instruction.symbol
                    security_holding.holding_qty = trade_instruction.quantity
                    security_holding.purchase_price = security_price
                else:
                    print("Security already exists")
                    security_holding_total_qty = security_holding.holding_qty + trade_instruction.quantity
                    security_holding.holding_qty = security_holding
                    security_holding.purchase_price = (
                        security_holding.purchase_price + security_price) / 2

                session.add(security_holding)

                accpunt_balance_payload = {"account_id": trade_instruction.account_id, "balance_amount": (
                    existing_account_balance - trade_value)}
                account_bal_service.add_update_account_balance(
                    session, payload=accpunt_balance_payload, commit=False)

                # call the method to update trade activity log

                session.flush()
                session.commit()

                self.return_payload['status'] = SUCCESS_CODE
                self.return_payload['message'] = trade_instruction.symbol + \
                    " trade executed successfully"
                return self.return_payload
            except SQLAlchemyError as exception:
                self.return_payload['status'] = FATAL_CODE
                print(exception)
                #self.return_payload['message'] = exception._message
                session.rollback()
                return self.return_payload

                # if trade_instruction.direction = 'S':
                # check number of securities to sell <= securities in holding
                # if okay:
                # start a transaction
                # subtract security holding qty
                # update account balance
                # call the method to update trade activity log
                # close the transaction
                # if not okay - return an error message

        return self.return_payload
