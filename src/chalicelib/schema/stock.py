from pydantic import BaseModel, ValidationError, validator


class SecuritySchema(BaseModel):
    name: str

    class Config:
        orm_mode = True
