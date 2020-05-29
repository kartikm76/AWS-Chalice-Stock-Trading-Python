from sqlalchemy import update
from chalicelib.model.account_balance import AccountBalanceORM
from chalicelib.schema.account_balance import AccountBalanceSchema
from pydantic import BaseModel, Field, ValidationError
from chalicelib.utils.object_serialize import SerializeObject
from chalicelib.utils.constants import SUCCESS_CODE, ERROR_CODE, FATAL_CODE
      
class AccountBalanceService:
    return_payload = {
        "status": None,
        "message": None        
    }

    def add_update_account_balance (self, session, payload, commit=True):
        try:
            account_balance_schema = AccountBalanceSchema.parse_obj(payload)
            print(account_balance_schema)            
            account_balance = session.query(AccountBalanceORM).filter(AccountBalanceORM.account_id == account_balance_schema.account_id).first()
            if account_balance is None:
                account_balance = AccountBalanceORM()
                account_balance.account_id = account_balance_schema.account_id
                account_balance.balance_amount = account_balance_schema.balance_amount            
            else:
                account_balance.balance_amount = account_balance_schema.balance_amount
            
            session.add(account_balance)

            if commit:
                session.commit()
            
            self.return_payload['status'] = SUCCESS_CODE
            self.return_payload['message'] = "Balance updated for account - " + str(account_balance_schema.account_id)
        except ValidationError as e:
                self.return_payload['status'] = FATAL_CODE
                self.return_payload['message'] = e.errors()        
        return self.return_payload

    def get_account_balance(self, session, account_id=None):
        self.account_id = account_id
                
        account_balance_dictionary = {}
        account_balance_list = []
        
        if self.account_id is None:
            account_balance_rows = session.query(AccountBalanceORM)
        else:
            account_balance_rows = session.query(AccountBalanceORM).filter(AccountBalanceORM.account_id == self.account_id)

        for each_row in  account_balance_rows:            
            account_balance_dictionary = {  'account_id':  each_row.account_id,
                                            'balance_amount': each_row.balance_amount }

            account_balance_list.append(account_balance_dictionary)
                    
        return account_balance_list