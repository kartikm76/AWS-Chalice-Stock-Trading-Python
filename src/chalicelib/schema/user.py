from pydantic import BaseModel, constr, ValidationError, validator
import re

from typing import List

class UserSchema(BaseModel):
    id: str
    name: str
    ssn: str
    
    class Config:
        orm_mode = True
    
    @validator('id', pre=True)
    def v_alphanumeric(cls, v):
        assert v.isalpha(), 'must be alphanumeric'
        return v

    @validator('ssn')
    def ssn_must_format(cls, v):        
        if bool(re.match(r'^(?!000|.+0{4})(?:\d{9}|\d{3}-\d{2}-\d{4})$', v)):
            print ("SSN is valid")
        else:
            raise ValueError("SSN is invalid")            
        return v