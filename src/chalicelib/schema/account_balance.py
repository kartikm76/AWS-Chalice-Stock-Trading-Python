from pydantic import BaseModel, constr, ValidationError, validator

class AccountBalanceSchema(BaseModel):
    account_id: int
    balance_amount: float
    
    class Config:
        orm_mode = True