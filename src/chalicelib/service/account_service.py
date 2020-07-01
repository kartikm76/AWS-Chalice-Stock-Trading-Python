import datetime
import json
from chalicelib.model.account import AccountORM
from chalicelib.utils.object_serialize import SerializeObject
from chalicelib.utils.constants import *


class AccountService:

    return_payload = {
        "code": None,
        "message": None
    }

    def add_account(self, session, payload):
        account_type = payload["type"]
        if account_type == 'CASH_TRD':
            last_account = session.query(AccountORM).order_by(
                AccountORM.id.desc()).limit(1)
            print("Last Account: ", last_account.scalar())

            if last_account.scalar():
                last_account_id = last_account[0].id
                print("Last Account ID: ", last_account_id)
                new_account_id = last_account_id + 1
            else:
                new_account_id = 10001

            account = session.query(AccountORM).filter(
                AccountORM.id == new_account_id).first()
            if not account:
                account = AccountORM()
                account.id = new_account_id
                account.type = account_type
                account.is_active = YES_CODE
                account.open_date = datetime.date.today()
                session.add(account)
                session.commit()
                self.return_payload['code'] = SUCCESS_CODE
                self.return_payload['message'] = "AccountId: " + \
                    str(account.id) + " successfully created"
            else:
                self.return_payload['code'] = FATAL_CODE
                self.return_payload['message'] = "An internal error occured.."
        return self.return_payload

    def get_account_details(self, session, account_id=None):
        self.account_id = account_id
        account_list = []
        account_dict = {}

        if self.account_id is None:
            accounts = session.query(AccountORM)
        else:
            accounts = session.query(AccountORM).filter(
                AccountORM.id == self.account_id)

        for account in accounts:
            account_dict = {'id':  account.id,
                            'type': account.type,
                            'open_date': SerializeObject.serialize_object(account.open_date),
                            'is_active': account.is_active}

            account_list.append(account_dict)

        return account_list
