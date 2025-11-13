from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    
    class Config:
        from_attributes = True 

class Token(BaseModel):
    access_token: str
    token_type: str