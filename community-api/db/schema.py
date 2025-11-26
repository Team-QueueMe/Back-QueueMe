from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: int
    email: EmailStr
    name: str | None = None
    
    class Config:
        from_attributes = True 

class Token(BaseModel):
    access_token: str
    token_type: str

class PostCreate(BaseModel):
    user_name: str
    message: str
    daily_progress_percentage: int

class PostResponse(BaseModel):
    post_id: int
    user_id: str # google id 
    user_name: str
    message: str
    daily_progress_percentage: int
    created_at: datetime

    class Config:
        from_attributes = True