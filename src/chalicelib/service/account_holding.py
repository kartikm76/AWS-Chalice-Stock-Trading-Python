import datetime
import json
from chalicelib.model.security_holding import SecurityHoldingORM
from chalicelib.utils.object_serialize import SerializeObject
from chalicelib.utils.constants import *


class AccountHoldingService:
    def get_account_holding(self, session, account_id):
        self.account_id = account_id
        holding_list = []
        holding_dict = {}

        holdings = session.query(SecurityHoldingORM).filter(
            SecurityHoldingORM.account_id == self.account_id)

        for holding in holdings:
            holding_dict = {'account_id':  holding.account_id,
                            'symbol': holding.security_symbol,
                            'holding_qty': holding.holding_qty,
                            'purchase_price': holding.purchase_price}

            holding_list.append(holding_dict)

        return holding_list
