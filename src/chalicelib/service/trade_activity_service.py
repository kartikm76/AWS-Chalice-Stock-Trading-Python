import json
import requests
from chalicelib.model.trade_activity import TradeActivityORM
from chalicelib.utils.constants import SUCCESS_CODE, ERROR_CODE, FATAL_CODE


class TradeActivityService:
    return_payload = {
        "status": None,
        "message": None
    }

    def log_trade_activity(self, session, account_id, security_symbol, transaction_qty, transaction_price, transaction_type_code, transaction_timestamp):
        try:
            trade_activity = TradeActivityORM()
            trade_activity.account_id = account_id
            trade_activity.security_symbol = security_symbol
            trade_activity.transaction_qty = transaction_qty
            trade_activity.security_price = transaction_price
            trade_activity.transaction_type_code = transaction_type_code
            trade_activity.transaction_timestamp = transaction_timestamp
            session.add(trade_activity)

            self.return_payload['status'] = SUCCESS_CODE
            self.return_payload['message'] = "Trade Activity updated for account - " + \
                str(account_id)
        except:
            self.return_payload['code'] = FATAL_CODE
            self.return_payload['message'] = "An internal error occured.."
        return self.return_payload
