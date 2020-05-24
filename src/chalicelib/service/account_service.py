from chalicelib.model.account import AccountORM
from pydantic import BaseModel, Field
from chalicelib.utils.object_serialize import SerializeObject


class AccountService:

    def get_account_details(self, session, account_id=None):
        self.account_id = account_id
        account_list = []
        account_dict = {}
        
        if self.account_id is None:            
            accounts = session.query(AccountORM)
        else:
            accounts = session.query(AccountORM).filter(AccountORM.id == self.account_id)

        for account in  accounts:
            account_dict = {'id':  account.id,
                            'type': account.type,
                            'open_date': SerializeObject.serialize_object(account.open_date),
                            'is_active': account.isActive}
                          
            account_list.append(account_dict)
        
        return account_list