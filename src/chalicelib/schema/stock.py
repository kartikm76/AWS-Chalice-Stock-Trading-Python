from pydantic import BaseModel, ValidationError, validator

class StockSchema(BaseModel):    
    name: str
    
    class Config:
        orm_mode = True