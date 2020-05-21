from chalicelib.model.account_balance import AccountBalanceORM
from chalicelib.utils.object_serialize import SerializeObject
      
class AccountBalanceService:
    def get_account_balance(self, session, account_id=None):
        self.account_id = account_id
        
        data_rows = None
        account_balance_dictionary = {}
        account_balance_list = []
        
        print ("comgin here")
        if self.account_id is None:            
            account_balance_rows = session.query(AccountBalanceORM)
        else:
            account_balance_rows = session.query(AccountBalanceORM).filter(AccountBalanceORM.account_id == self.account_id)

        for each_row in  account_balance_rows:
            account_balance_dictionary = {  'account_id':  each_row.account_id,
                                            'balance_amount': each_row.balance_amount,
                                            'as_of_date': SerializeObject.serialize_object(each_row.as_of_date)}
                          
            account_balance_list.append(account_balance_dictionary)
                    
        return account_balance_list