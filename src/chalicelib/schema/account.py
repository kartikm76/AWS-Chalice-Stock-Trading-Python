from pydantic import BaseModel, constr, ValidationError, validator

class AccountSchema(BaseModel):    
    type: str
    
    class Config:
        orm_mode = True