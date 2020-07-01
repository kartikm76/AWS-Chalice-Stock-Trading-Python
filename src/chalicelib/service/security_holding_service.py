from chalicelib.model.security_holding import SecurityHoldingORM
from chalicelib.utils.constants import SUCCESS_CODE, ERROR_CODE, FATAL_CODE


class SecurityHoldingService:
    return_payload = {
        "status": None,
        "message": None
    }

    def get_security_holding(self, session, account_id, security_symbol):
        security_holding = session.query(SecurityHoldingORM).filter((SecurityHoldingORM.account_id == account_id)
                                                                    & (SecurityHoldingORM.security_symbol == security_symbol)).first()

        return security_holding

    def add_update_security_holding(self, session, account_id, security_symbol, security_type_code, transaction_qty, transaction_price):
        security_holding = get_security_holding(
            session, account_id, security_symbol)

        if security_holding is None:
            security_holding = SecurityHoldingORM()
            security_holding.account_id = account_id
            security_holding.security_symbol = security_symbol
            security_holding.security_type_code = security_type_code
            security_holding.holding_qty = transaction_qty
            security_holding.purchase_price = transaction_price
            session.add(security_holding)
            self.return_payload['status'] = SUCCESS_CODE
            self.return_payload['message'] = "Security Holding added for account - " + str(
                account_id)
        else:
            print("Security already exists")
            security_holding.holding_qty = security_holding.holding_qty + \
                transaction_qty
            security_holding.purchase_price = (
                security_holding.purchase_price + transaction_price) / 2
            self.return_payload['status'] = SUCCESS_CODE
            self.return_payload['message'] = "Security Holding updated for account - " + str(
                account_id)
        return self.return_payload
