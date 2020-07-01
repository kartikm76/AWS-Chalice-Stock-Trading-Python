import datetime
from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from chalicelib.model.security_holding import SecurityHoldingORM
from chalicelib.model.account_balance import AccountBalanceORM
from chalicelib.schema.trade import TradeSchema
from chalicelib.service.account_balance_service import AccountBalanceService
from chalicelib.service.security_lookup_service import SecurityLookUpService
from chalicelib.service.security_holding_service import SecurityHoldingService
from chalicelib.service.trade_activity_service import TradeActivityService
from chalicelib.utils.constants import API_KEY, SUCCESS_CODE, ERROR_CODE, FATAL_CODE


class TradeService:

    return_payload = {
        "status": None,
        "message": None
    }

    def trade(self, session, payload):
        trade_instruction = ""
        trade_value = ""
        security_price = 0.0

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
                # Add / Update Security Holding
                SecurityHoldingService().add_update_security_holding(session=session,
                                                                     account_id=trade_instruction.account_id,
                                                                     security_symbol=trade_instruction.symbol,
                                                                     security_type_code="STOCK",
                                                                     transaction_qty=trade_instruction.quantity,
                                                                     transaction_price=security_price)

                # Update Account Balance
                account_balance_payload = {"account_id": trade_instruction.account_id, "balance_amount": (
                    existing_account_balance - trade_value)}
                account_bal_service.add_update_account_balance(
                    session, payload=account_balance_payload)

            except SQLAlchemyError as exception:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = '[KM] An internal error occurred..'
                #self.return_payload['message'] = exception._message
                print(exception)
                session.rollback()
                return self.return_payload

        if trade_instruction.direction == 'S':
            # Exit; if security is not being held
            # check number of securities to sell <= securities in holding
            security_holding = SecurityHoldingService().get_security_holding(session=session,
                                                                             account_id=trade_instruction.account_id,
                                                                             security_symbol=trade_instruction.symbol)
            if security_holding is None:
                self.return_payload['status'] = ERROR_CODE
                self.return_payload['message'] = "Security not being held: " + \
                    trade_instruction.symbol
                return self.return_payload

            # start a transaction
            try:
                # Add / Update Security Holding
                SecurityHoldingService().add_update_security_holding(session=session,
                                                                     account_id=trade_instruction.account_id,
                                                                     security_symbol=trade_instruction.symbol,
                                                                     security_type_code="STOCK",
                                                                     transaction_qty=trade_instruction.quantity,
                                                                     transaction_price=security_price)

                # Update Account Balance
                account_balance_payload = {"account_id": trade_instruction.account_id, "balance_amount": (
                    existing_account_balance + trade_value)}
                account_bal_service.add_update_account_balance(
                    session, payload=account_balance_payload)
            except SQLAlchemyError as exception:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = '[KM] An internal error occurred..'
                #self.return_payload['message'] = exception._message
                print(exception)
                session.rollback()
                return self.return_payload

        # Log the trade activity
        TradeActivityService().log_trade_activity(session=session,
                                                  account_id=trade_instruction.account_id,
                                                  security_symbol=trade_instruction.symbol,
                                                  transaction_qty=trade_instruction.quantity,
                                                  transaction_price=security_price,
                                                  transaction_type_code='B',
                                                  transaction_timestamp=datetime.datetime.now())

        session.flush()
        session.commit()

        self.return_payload['status'] = SUCCESS_CODE
        self.return_payload['message'] = trade_instruction.symbol + \
            " trade executed successfully"
        return self.return_payload
