from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostCreate(BaseModel):
    message: str

class PostResponse(BaseModel):
    post_id: int
    user_id: str
    user_name: str
    message: str
    daily_progress_percentage: int
    created_at: datetime

    class Config:
        from_attributes = True